import 'package:flutter/material.dart';

/// Legend widget to show header names with their associated color
class ScaleLegend extends StatelessWidget {
  /// Map of header name -> Color
  final Map<String, Color> headerColors;

  const ScaleLegend({super.key, required this.headerColors});

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

        // Estimate how many columns we’d need
        int totalEntries = orderedEntries.length;
        int estimatedColumns = (totalEntries / rowsPerColumn).ceil();

        // Rough width per column
        double charWidth = fontSize * 0.6;
        double textWidth = 25 * charWidth;
        double columnWidth = textWidth + 24 + 12 + 32; // text + box + padding

        // If too wide, reduce font size and allow more rows
        while (estimatedColumns * columnWidth > constraints.maxWidth && fontSize > 12) {
          fontSize -= 1; // shrink text
          rowsPerColumn += 1; // allow more rows
          estimatedColumns = (totalEntries / rowsPerColumn).ceil();

          charWidth = fontSize * 0.6;
          textWidth = 25 * charWidth;
          columnWidth = textWidth + 24 + 12 + 32;
        }

        // Break into chunks with adjusted rowsPerColumn
        final chunks = _chunkEntries(orderedEntries, rowsPerColumn);

        return Align(
          alignment: Alignment.topCenter,
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            padding: const EdgeInsets.only(top: 16.0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: chunks.map((chunk) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 32.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: chunk.map((entry) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6.0),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              // Color box
                              Container(
                                width: 24,
                                height: 24,
                                decoration: BoxDecoration(
                                  color: entry.value,
                                  border: Border.all(color: Colors.black),
                                ),
                              ),
                              const SizedBox(width: 12),
                              // Fixed-width text
                              SizedBox(
                                width: textWidth,
                                child: Text(
                                  entry.key.padRight(25),
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
        );
      },
    );
  }
}
