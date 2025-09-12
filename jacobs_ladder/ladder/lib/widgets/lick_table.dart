import 'package:flutter/material.dart';
import '../../models/licks.dart';
import '../../widgets/play_button.dart';

class LickTable extends StatelessWidget {
  final String genre;
  final List<Lick> licks;
  final Function(Lick) onDelete;

  const LickTable({
    super.key,
    required this.genre,
    required this.licks,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: DataTable(
        columnSpacing: 20,
        headingRowColor: MaterialStateProperty.all(const Color.fromARGB(255, 52, 64, 52)),
        columns: const [
          DataColumn(label: Text("Name")),
          DataColumn(label: Text("Type")),
          DataColumn(label: Text("Length (s)")),
          DataColumn(label: Text("Play")),
          DataColumn(label: Text("")), // delete column
        ],
        rows: licks.map((lick) {
          return DataRow(
            color: MaterialStateProperty.resolveWith<Color?>(
              (Set<MaterialState> states) {
                if (states.contains(MaterialState.hovered)) return Colors.grey[800];
                return null;
              },
            ),
            cells: [
              DataCell(Text(lick.name)),
              DataCell(Text(lick.type)),
              DataCell(Text(lick.length.toStringAsFixed(1))),
              DataCell(PlayButton(lick: lick)),
              DataCell(
                IconButton(
                  icon: const Icon(Icons.delete, color: Colors.red),
                  onPressed: () => onDelete(lick),
                ),
              ),
            ],
          );
        }).toList(),
      ),
    );
  }
}
