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

    // Break into columns of 5
    final chunks = _chunkEntries(orderedEntries, 5);

    // Approximate width for 25 characters at fontSize 24
    const double charWidth = 10;
    const double textWidth = 25 * charWidth;

    return Align(
      alignment: Alignment.topCenter,
      child: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        padding: const EdgeInsets.only(top: 16.0),
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
                            style: const TextStyle(
                              fontSize: 24,
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
    );
  }
}
