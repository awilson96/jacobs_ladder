import 'package:flutter/material.dart';
import '../../models/licks.dart';
import '../../widgets/play_button.dart';

class LickTable extends StatefulWidget {
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
  State<LickTable> createState() => _LickTableState();
}

class _LickTableState extends State<LickTable> {
  int? _hoveredRowIndex;
  int? _selectedRowIndex;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      scrollDirection: Axis.horizontal,
      child: IntrinsicWidth(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Table header
            Container(
              color: const Color.fromARGB(255, 52, 64, 52),
              padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: const [
                  SizedBox(width: 48, child: Text("Play", style: TextStyle(fontWeight: FontWeight.bold))),
                  SizedBox(width: 150, child: Text("Name", style: TextStyle(fontWeight: FontWeight.bold))),
                  SizedBox(width: 100, child: Text("Type", style: TextStyle(fontWeight: FontWeight.bold))),
                  SizedBox(width: 80, child: Text("Length (s)", style: TextStyle(fontWeight: FontWeight.bold))),
                  SizedBox(width: 40), // delete column
                ],
              ),
            ),
            // Table rows
            ...List.generate(widget.licks.length, (index) {
              final lick = widget.licks[index];
              final isHovered = _hoveredRowIndex == index;
              final isSelected = _selectedRowIndex == index;
              final highlight = isHovered || isSelected;

              return MouseRegion(
                onEnter: (_) => setState(() => _hoveredRowIndex = index),
                onExit: (_) => setState(() => _hoveredRowIndex = null),
                child: GestureDetector(
                  onTap: () {
                    setState(() {
                      if (_selectedRowIndex == index) {
                        _selectedRowIndex = null;
                      } else {
                        _selectedRowIndex = index;
                      }
                    });
                  },
                  child: Container(
                    color: highlight ? Colors.grey[800] : Colors.transparent,
                    padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 4),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(width: 48, child: PlayButton(lick: lick)),
                        SizedBox(width: 150, child: Text(lick.name)),
                        SizedBox(width: 100, child: Text(lick.type)),
                        SizedBox(width: 80, child: Text(lick.length.toStringAsFixed(1))),
                        SizedBox(
                          width: 40,
                          child: isHovered
                              ? IconButton(
                                  icon: const Icon(Icons.delete, color: Colors.red),
                                  onPressed: () => widget.onDelete(lick),
                                  padding: EdgeInsets.zero,
                                  constraints: const BoxConstraints(),
                                )
                              : null,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}
