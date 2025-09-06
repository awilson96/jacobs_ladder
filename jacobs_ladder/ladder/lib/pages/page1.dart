import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../widgets/piano.dart';

/// A simple widget to display the legend of headers with their colors
class PianoLegend extends StatelessWidget {
  final Map<String, Color> headerColors;

  const PianoLegend({super.key, required this.headerColors});

  @override
  Widget build(BuildContext context) {
    // Fixed positions for up to 6 headers (can expand as needed)
    final positions = [
      Alignment.topCenter,
      Alignment.topLeft,
      Alignment.topRight,
      Alignment.centerLeft,
      Alignment.centerRight,
      Alignment.bottomCenter,
    ];

    List<Widget> legendItems = [];
    int index = 0;
    headerColors.forEach((header, color) {
      if (index >= positions.length) return; // ignore overflow for now
      legendItems.add(
        Align(
          alignment: positions[index],
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 20,
                  height: 20,
                  decoration: BoxDecoration(
                    color: color,
                    border: Border.all(color: Colors.black),
                  ),
                ),
                const SizedBox(width: 6),
                Text(header, style: const TextStyle(fontSize: 16)),
              ],
            ),
          ),
        ),
      );
      index++;
    });

    return Stack(children: legendItems);
  }
}

/// Page1 with Piano and legend
class Page1 extends StatefulWidget {
  const Page1({super.key});

  @override
  State<Page1> createState() => _Page1State();
}

class _Page1State extends State<Page1> {
  // Map of header -> color (LIVE_KEYS always yellow)
  final Map<String, Color> legendColors = {'LIVE_KEYS': Colors.yellow};

  /// Callback passed to Piano widget
  void updateLegend(Map<String, Uint8List> suggestions) {
    setState(() {
      for (var header in suggestions.keys) {
        // Assign a default color for new headers (orange here)
        if (!legendColors.containsKey(header)) {
          legendColors[header] = Colors.orange;
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Legend at fixed positions
          PianoLegend(headerColors: legendColors),

          // Piano anchored to the bottom-center
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Center(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Piano(
                  onSuggestionUpdate: updateLegend,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
