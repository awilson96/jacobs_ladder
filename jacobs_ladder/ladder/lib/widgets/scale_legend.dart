import 'package:flutter/material.dart';

/// Legend widget to show header names with their associated color
/// Supports clicking to filter by a single scale
class ScaleLegend extends StatefulWidget {
  /// Map of header name -> Color
  final Map<String, Color> headerColors;

  /// Horizontal nudge to adjust centering (in pixels)
  final double horizontalNudge;

  /// Callback when user clicks a header: sends the selected header or null if deselected
  final ValueChanged<String?>? onHeaderSelected;

  const ScaleLegend({
    super.key,
    required this.headerColors,
    this.horizontalNudge = 0.0,
    this.onHeaderSelected,
  });

  @override
  _ScaleLegendState createState() => _ScaleLegendState();
}

class _ScaleLegendState extends State<ScaleLegend> {
  String? selectedHeader;

  /// Helper: split list into chunks of size [chunkSize]
  List<List<MapEntry<String, Color>>> _chunkEntries(
      List<MapEntry<String, Color>> entries, int chunkSize) {
    List<List<MapEntry<String, Color>>> chunks = [];
    for (var i = 0; i < entries.length; i += chunkSize) {
      chunks.add(entries.sublist(
          i, i + chunkSize > entries.length ? entries.length : i + chunkSize));
    }
    return chunks;
  }

  void _onHeaderTap(String header) {
    setState(() {
      if (selectedHeader == header) {
        selectedHeader = null; // deselect
      } else {
        selectedHeader = header;
      }
    });

    if (widget.onHeaderSelected != null) {
      widget.onHeaderSelected!(selectedHeader);
    }
  }

  @override
  Widget build(BuildContext context) {
    // Always keep "Live keys" first
    final orderedEntries = widget.headerColors.entries.toList()
      ..sort((a, b) {
        if (a.key == 'Live keys') return -1;
        if (b.key == 'Live keys') return 1;
        return 0;
      });

    return LayoutBuilder(
      builder: (context, constraints) {
        double fontSize = 24;
        int rowsPerColumn = 5;

        int totalEntries = orderedEntries.length;
        int estimatedColumns = (totalEntries / rowsPerColumn).ceil();

        double charWidth = fontSize * 0.6;

        int maxHeaderLength = orderedEntries
            .map((e) => e.key.length)
            .reduce((a, b) => a > b ? a : b);
        double textWidth = maxHeaderLength * charWidth;
        double columnWidth = textWidth + 24 + 12 + 32;

        while (estimatedColumns * columnWidth > constraints.maxWidth &&
            fontSize > 12) {
          fontSize -= 1;
          rowsPerColumn += 1;
          estimatedColumns = (totalEntries / rowsPerColumn).ceil();
          charWidth = fontSize * 0.6;
          maxHeaderLength = orderedEntries
              .map((e) => e.key.length)
              .reduce((a, b) => a > b ? a : b);
          textWidth = maxHeaderLength * charWidth;
          columnWidth = textWidth + 24 + 12 + 32;
        }

        final chunks = _chunkEntries(orderedEntries, rowsPerColumn);

        return Align(
          alignment: Alignment.topCenter,
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            padding: const EdgeInsets.only(top: 16.0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Padding(
                padding: EdgeInsets.only(left: widget.horizontalNudge),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: chunks.map((chunk) {
                    int chunkMaxLength =
                        chunk.map((e) => e.key.length).reduce((a, b) => a > b ? a : b);
                    double chunkTextWidth = chunkMaxLength * charWidth;

                    return Padding(
                      padding: const EdgeInsets.only(right: 16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: chunk.map((entry) {
                          final isSelected = entry.key == selectedHeader;
                          return GestureDetector(
                            onTap: () => _onHeaderTap(entry.key),
                            child: Padding(
                              padding: const EdgeInsets.symmetric(vertical: 6.0),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Container(
                                    width: 24,
                                    height: 24,
                                    decoration: BoxDecoration(
                                      color: entry.value,
                                      border: Border.all(
                                        color: isSelected ? Colors.yellow : Colors.black,
                                        width: isSelected ? 3 : 1,
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 12),
                                  SizedBox(
                                    width: chunkTextWidth,
                                    child: Text(
                                      entry.key,
                                      style: TextStyle(
                                        fontSize: fontSize,
                                        fontWeight: FontWeight.bold,
                                        color: isSelected ? Colors.yellow : Colors.white,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
