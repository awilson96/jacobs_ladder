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

  // Settings state
  bool showMajor = true;
  bool showHarmonicMinor = true;
  bool showHarmonicMajor = true;
  bool showMelodicMinor = true;

  // Keep latest suggestions so we can re-filter instantly
  Map<String, Uint8List> latestSuggestions = {};

  /// Helper to determine if a header should be filtered
  bool _shouldIncludeHeader(String header) {
    if (header == 'Live keys') return true;

    if (header.contains('Harmonic Minor')) return showHarmonicMinor;
    if (header.contains('Harmonic Major')) return showHarmonicMajor;
    if (header.contains('Melodic Minor')) return showMelodicMinor;

    // Detect "X Major" (e.g., "C Major") – first character + space + Major
    final majorPattern = RegExp(r'^[A-G][b#]?\sMajor');
    if (majorPattern.hasMatch(header)) return showMajor;

    return true; // default allow
  }

  /// Updates the legend with filtered suggestions
  void updateLegend(Map<String, Uint8List> suggestions) {
    latestSuggestions = suggestions; // cache for instant filter updates

    _applyFilters();
  }

  /// Apply current filter settings to the cached suggestions
  void _applyFilters() {
    setState(() {
      Map<String, Color> newLegendColors = {'Live keys': Colors.red};
      int colorIndex = 0;

      for (var header in latestSuggestions.keys) {
        if (!_shouldIncludeHeader(header)) continue;
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
      appBar: AppBar(
        title: const Text("Page 1"),
        actions: [
          Builder(
            builder: (context) => IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () {
                Scaffold.of(context).openEndDrawer();
              },
            ),
          )
        ],
      ),
      endDrawer: Drawer(
        child: ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            const Text(
              "Scale Filters",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const Divider(),
            CheckboxListTile(
              title: const Text("Major Scales"),
              value: showMajor,
              onChanged: (val) {
                setState(() {
                  showMajor = val ?? true;
                  _applyFilters(); // reapply immediately
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Harmonic Minor Scales"),
              value: showHarmonicMinor,
              onChanged: (val) {
                setState(() {
                  showHarmonicMinor = val ?? true;
                  _applyFilters();
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Harmonic Major Scales"),
              value: showHarmonicMajor,
              onChanged: (val) {
                setState(() {
                  showHarmonicMajor = val ?? true;
                  _applyFilters();
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Melodic Minor Scales"),
              value: showMelodicMinor,
              onChanged: (val) {
                setState(() {
                  showMelodicMinor = val ?? true;
                  _applyFilters();
                });
              },
            ),
          ],
        ),
      ),
      body: Stack(
        children: [
          // ScaleLegend with vertical stacking
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
