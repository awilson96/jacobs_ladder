import 'package:flutter/material.dart';

/// Legend widget to show header names with their associated color
class ScaleLegend extends StatelessWidget {
  /// Map of header name -> Color
  final Map<String, Color> headerColors;

  /// Horizontal nudge to adjust centering (in pixels)
  final double horizontalNudge;

  const ScaleLegend({
    super.key,
    required this.headerColors,
    this.horizontalNudge = 0.0, // default no nudge
  });

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

  @override
  Widget build(BuildContext context) {
    // Always keep "Live keys" first
    final orderedEntries = headerColors.entries.toList()
      ..sort((a, b) {
        if (a.key == 'Live keys') return -1;
        if (b.key == 'Live keys') return 1;
        return 0;
      });

    return LayoutBuilder(
      builder: (context, constraints) {
        // Default font size and rows
        double fontSize = 24;
        int rowsPerColumn = 5;

        int totalEntries = orderedEntries.length;
        int estimatedColumns = (totalEntries / rowsPerColumn).ceil();

        double charWidth = fontSize * 0.6;

        // Compute max header length for dynamic width
        int maxHeaderLength = orderedEntries.map((e) => e.key.length).reduce((a, b) => a > b ? a : b);
        double textWidth = maxHeaderLength * charWidth;

        // Column width including color box, spacing, and padding
        double columnWidth = textWidth + 24 + 12 + 32;

        // Shrink font if too wide
        while (estimatedColumns * columnWidth > constraints.maxWidth && fontSize > 12) {
          fontSize -= 1;
          rowsPerColumn += 1;
          estimatedColumns = (totalEntries / rowsPerColumn).ceil();
          charWidth = fontSize * 0.6;
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
                padding: EdgeInsets.only(left: horizontalNudge),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: chunks.map((chunk) {
                    // Compute max header length per chunk for dynamic width per column
                    int chunkMaxLength = chunk.map((e) => e.key.length).reduce((a, b) => a > b ? a : b);
                    double chunkTextWidth = chunkMaxLength * charWidth;

                    return Padding(
                      padding: const EdgeInsets.only(right: 16.0), // reduced spacing
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: chunk.map((entry) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 6.0),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Container(
                                  width: 24,
                                  height: 24,
                                  decoration: BoxDecoration(
                                    color: entry.value,
                                    border: Border.all(color: Colors.black),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                SizedBox(
                                  width: chunkTextWidth,
                                  child: Text(
                                    entry.key, // no padRight needed
                                    style: TextStyle(
                                      fontSize: fontSize,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ],
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
