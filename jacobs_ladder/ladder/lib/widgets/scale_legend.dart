import 'package:flutter/material.dart';

/// Legend widget to show header names with their associated color
class ScaleLegend extends StatelessWidget {
  /// Map of header name -> Color
  final Map<String, Color> headerColors;

  const ScaleLegend({super.key, required this.headerColors});

  @override
  Widget build(BuildContext context) {
    // Predefined fixed positions for each legend item
    final positions = <Alignment>[
      Alignment.topCenter,
      Alignment.centerLeft,
      Alignment.centerRight,
      Alignment.bottomCenter,
      Alignment.topLeft,
      Alignment.topRight,
      Alignment.bottomLeft,
      Alignment.bottomRight,
    ];

    int i = 0;
    return Stack(
      children: headerColors.entries.map((entry) {
        final alignment = positions[i % positions.length];
        final widget = Align(
          alignment: alignment,
          child: Padding(
            padding: const EdgeInsets.all(8.0),
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
                const SizedBox(width: 4),
                // Header text
                Text(
                  entry.key,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        );
        i++;
        return widget;
      }).toList(),
    );
  }
}
