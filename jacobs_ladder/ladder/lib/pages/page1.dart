import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../widgets/piano.dart';
import '../widgets/scale_legend.dart';

/// Page1 with Piano and vertical stacked legend
class Page1 extends StatefulWidget {
  const Page1({super.key});

  @override
  State<Page1> createState() => _Page1State();
}

class _Page1State extends State<Page1> {
  // Map of header -> Color (Live keys always yellow)
  Map<String, Color> legendColors = {'Live keys': Colors.red};

  // Default colors to cycle for new suggestions
  final List<Color> suggestionColors = [
    Colors.orange,
    Colors.yellow,
    Colors.green,
    Colors.teal,
    Colors.blue,
    Colors.purple,
    Colors.pink,
  ];

  /// Callback passed to Piano widget to update legend
  void updateLegend(Map<String, Uint8List> suggestions) {
    setState(() {
      Map<String, Color> newLegendColors = {'Live keys': Colors.red};

      int colorIndex = 0;
      for (var header in suggestions.keys) {
        if (header == 'Live keys') continue;
        newLegendColors[header] =
            suggestionColors[colorIndex % suggestionColors.length];
        colorIndex++;
      }

      legendColors = newLegendColors;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Use the updated ScaleLegend with vertical stacking
          ScaleLegend(headerColors: legendColors),

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
