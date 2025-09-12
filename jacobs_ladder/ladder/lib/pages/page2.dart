import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/gestures.dart';

import '../models/licks.dart';
import '../widgets/play_button.dart';

class Page2 extends StatefulWidget {
  const Page2({super.key});

  @override
  State<Page2> createState() => _Page2State();
}

class _Page2State extends State<Page2> {
  final List<String> genres = const [
    "Rock",
    "Pop",
    "Jazz",
    "Hip-Hop",
    "Classical",
    "Electronic",
    "Country",
    "Reggae",
    "Blues",
    "Metal",
  ];

  final Map<String, List<Lick>> genreLicks = {
    "Rock": [
      Lick(id: 1, name: "Power Riff", type: "Melody", length: 12.3),
      Lick(id: 2, name: "Groove Bass", type: "Bassline", length: 8.5),
    ],
    "Jazz": [
      Lick(id: 1, name: "Swing Line", type: "Harmony", length: 15.0),
      Lick(id: 2, name: null, type: "Chords", length: 10.2),
    ],
  };

  final ScrollController _scrollController = ScrollController();
  bool _hovering = false;

  void _showAddDialog(BuildContext context, String genre) {
    final formKey = GlobalKey<FormState>();
    String? name;
    String? type;
    double? length;
    String? midiPath;

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Add New Lick"),
          content: Form(
            key: formKey,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextFormField(
                    decoration: const InputDecoration(labelText: "Name (optional)"),
                    onSaved: (val) => name = val,
                  ),
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
                  TextFormField(
                    decoration: const InputDecoration(labelText: "Length (s)"),
                    keyboardType: TextInputType.number,
                    validator: (val) {
                      if (val == null || val.isEmpty) return "Required";
                      if (double.tryParse(val) == null) return "Must be a number";
                      return null;
                    },
                    onSaved: (val) => length = double.tryParse(val!),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () async {
                      FilePickerResult? result = await FilePicker.platform.pickFiles(
                        type: FileType.custom,
                        allowedExtensions: ['mid', 'midi'],
                      );
                      if (result != null && result.files.single.path != null) {
                        setState(() {
                          midiPath = result.files.single.path;
                        });
                      }
                    },
                    child: Text(midiPath == null ? "Select MIDI file" : "Selected"),
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
                if (formKey.currentState!.validate()) {
                  formKey.currentState!.save();

                  final currentList = genreLicks[genre] ?? [];
                  final newId = currentList.length + 1;

                  final newLick = Lick(
                    id: newId,
                    name: name,
                    type: type!,
                    length: length!,
                    midiPath: midiPath,
                  );

                  setState(() {
                    genreLicks.putIfAbsent(genre, () => []);
                    genreLicks[genre]!.add(newLick);
                  });

                  Navigator.pop(context);
                }
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final tabWidth = screenWidth / 7;

    return DefaultTabController(
      length: genres.length,
      child: Scaffold(
        body: Column(
          children: [
            SizedBox(
              height: 60,
              child: Listener(
                onPointerSignal: (pointerSignal) {
                  if (pointerSignal is PointerScrollEvent) {
                    final newOffset = (_scrollController.offset + pointerSignal.scrollDelta.dy)
                        .clamp(0.0, _scrollController.position.maxScrollExtent);
                    _scrollController.jumpTo(newOffset);
                  }
                },
                child: MouseRegion(
                  onEnter: (_) => setState(() => _hovering = true),
                  onExit: (_) => setState(() => _hovering = false),
                  child: Scrollbar(
                    controller: _scrollController,
                    thumbVisibility: _hovering,
                    thickness: 4,
                    radius: const Radius.circular(8),
                    child: SingleChildScrollView(
                      controller: _scrollController,
                      scrollDirection: Axis.horizontal,
                      physics: const BouncingScrollPhysics(),
                      child: TabBar(
                        isScrollable: true,
                        indicatorColor: Theme.of(context).colorScheme.primary,
                        tabs: genres
                            .map((genre) => SizedBox(width: tabWidth, child: Tab(text: genre)))
                            .toList(),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              child: TabBarView(
                children: genres.map((genre) {
                  final licks = genreLicks[genre] ?? [];
                  return SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: DataTable(
                      columnSpacing: 20,
                      headingRowColor:
                          MaterialStateProperty.all(const Color.fromARGB(255, 52, 64, 52)),
                      columns: const [
                        DataColumn(label: Text("ID")),
                        DataColumn(label: Text("Name")),
                        DataColumn(label: Text("Type")),
                        DataColumn(label: Text("Length (s)")),
                        DataColumn(label: Text("Play")),
                        DataColumn(label: Text("")), // Empty header for delete
                      ],
                      rows: licks.map((lick) {
                        return DataRow(
                          color: MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (states.contains(MaterialState.hovered)) {
                                return Colors.grey[800];
                              }
                              return null;
                            },
                          ),
                          cells: [
                            DataCell(Text(lick.id.toString())),
                            DataCell(Text(lick.name ?? "—")),
                            DataCell(Text(lick.type)),
                            DataCell(Text(lick.length.toStringAsFixed(1))),
                            DataCell(PlayButton(lick: lick)),
                            DataCell(
                              IconButton(
                                icon: const Icon(Icons.delete, color: Colors.red),
                                onPressed: () {
                                  setState(() {
                                    genreLicks[genre]?.remove(lick);
                                    // Reindex IDs
                                    final list = genreLicks[genre]!;
                                    for (int i = 0; i < list.length; i++) {
                                      list[i] = Lick(
                                        id: i + 1,
                                        name: list[i].name,
                                        type: list[i].type,
                                        length: list[i].length,
                                        midiPath: list[i].midiPath,
                                      );
                                    }
                                  });
                                },
                              ),
                            ),
                          ],
                        );
                      }).toList(),
                    ),
                  );
                }).toList(),
              ),
            ),
          ],
        ),
        floatingActionButton: Builder(
          builder: (context) {
            return FloatingActionButton(
              onPressed: () => _showAddDialog(
                context,
                genres[DefaultTabController.of(context)!.index],
              ),
              child: const Icon(Icons.add),
            );
          },
        ),
      ),
    );
  }
}
