import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../models/licks.dart';

// TODO: Implement actual MIDI length calculation
Future<double> getMidiLength(String path) async {
  // Placeholder: return dummy value
  return 10.0;
}

Future<void> showAddLickDialog(
  BuildContext context, {
  required String genre,
  required Function(Lick) onAdd,
}) async {
  final formKey = GlobalKey<FormState>();
  String? name;
  String? type;
  String? midiPath;
  double? length;
  String? midiError;

  await showDialog(
    context: context,
    builder: (context) {
      return StatefulBuilder(
        builder: (context, setState) {
          return AlertDialog(
            title: const Text("Add New Lick"),
            content: Form(
              key: formKey,
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Name (required)
                    TextFormField(
                      decoration: const InputDecoration(labelText: "Name"),
                      validator: (val) =>
                          val == null || val.isEmpty ? "Required" : null,
                      onSaved: (val) => name = val,
                    ),
                    const SizedBox(height: 8),
                    // Type (required)
                    DropdownButtonFormField<String>(
                      decoration: const InputDecoration(labelText: "Type"),
                      items: const [
                        DropdownMenuItem(value: "Melody", child: Text("Melody")),
                        DropdownMenuItem(value: "Chords", child: Text("Chords")),
                        DropdownMenuItem(value: "Harmony", child: Text("Harmony")),
                        DropdownMenuItem(value: "Bassline", child: Text("Bassline")),
                      ],
                      validator: (val) => val == null ? "Required" : null,
                      onChanged: (val) => type = val,
                    ),
                    const SizedBox(height: 16),
                    // MIDI file picker
                    ElevatedButton(
                      onPressed: () async {
                        FilePickerResult? result = await FilePicker.platform.pickFiles(
                          type: FileType.custom,
                          allowedExtensions: ['mid', 'midi'],
                        );
                        if (result != null && result.files.single.path != null) {
                          final path = result.files.single.path!;
                          final midiLength = await getMidiLength(path);
                          setState(() {
                            midiPath = path;
                            length = midiLength;
                            midiError = null; // clear previous error
                          });
                        }
                      },
                      child: Text(midiPath == null ? "Select MIDI file" : "Selected"),
                    ),
                    // Error message if no MIDI selected
                    if (midiError != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(
                          midiError!,
                          style: const TextStyle(color: Colors.red),
                        ),
                      ),
                  ],
                ),
              ),
            ),
            actions: [
              TextButton(
                child: const Text("Cancel"),
                onPressed: () => Navigator.pop(context),
              ),
              ElevatedButton(
                child: const Text("Add"),
                onPressed: () {
                  final isValid = formKey.currentState!.validate();
                  if (!isValid) return;

                  if (midiPath == null || length == null) {
                    setState(() {
                      midiError = "MIDI file is required";
                    });
                    return;
                  }

                  formKey.currentState!.save();
                  final newLick = Lick(
                    name: name!,
                    type: type!,
                    length: length!,
                    midiPath: midiPath,
                  );
                  onAdd(newLick);
                  Navigator.pop(context);
                },
              ),
            ],
          );
        },
      );
    },
  );
}
