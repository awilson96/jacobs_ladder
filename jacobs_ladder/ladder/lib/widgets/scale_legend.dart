import 'package:flutter/material.dart';

/// Legend widget to show header names with their associated color
class ScaleLegend extends StatelessWidget {
  /// Map of header name -> Color
  final Map<String, Color> headerColors;

  const ScaleLegend({super.key, required this.headerColors});

  @override
  Widget build(BuildContext context) {
    // Order headers to make sure Live keys is always first
    final orderedEntries = headerColors.entries.toList()
      ..sort((a, b) {
        if (a.key == 'Live keys') return -1;
        if (b.key == 'Live keys') return 1;
        return 0;
      });

    // Approximate width for 25 characters at fontSize 14
    const double charWidth = 8; // adjust if needed
    const double textWidth = 25 * charWidth;

    // Offset to visually center the legend despite padding spaces
    const double leftOffset = 12 * charWidth;

    return Align(
      alignment: Alignment.topCenter, // center the column horizontally
      child: Padding(
        padding: const EdgeInsets.only(top: 16.0, left: leftOffset),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start, // left-align items in the column
          children: orderedEntries.map((entry) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4.0),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Color box
                  Container(
                    width: 16,
                    height: 16,
                    decoration: BoxDecoration(
                      color: entry.value,
                      border: Border.all(color: Colors.black),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Fixed-width text
                  SizedBox(
                    width: textWidth,
                    child: Text(
                      entry.key.padRight(25), // ensure 25 characters
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}
