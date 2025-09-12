import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../widgets/piano.dart';
import '../widgets/scale_legend.dart';
import '../services/settings_service.dart';

/// Page1 with Piano, vertical stacked legend, and persistent settings
class Page1 extends StatefulWidget {
  const Page1({super.key});

  @override
  State<Page1> createState() => _Page1State();
}

class _Page1State extends State<Page1> {
  // Map of header -> Color (Live keys always red)
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

  final SettingsService _settingsService = SettingsService();

  @override
  void initState() {
    super.initState();
    _loadFilters();
  }

  Future<void> _loadFilters() async {
    final major = await _settingsService.getShowMajor();
    final harmonicMinor = await _settingsService.getShowHarmonicMinor();
    final harmonicMajor = await _settingsService.getShowHarmonicMajor();
    final melodicMinor = await _settingsService.getShowMelodicMinor();

    // Defer the setState to avoid calling during build
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      setState(() {
        showMajor = major;
        showHarmonicMinor = harmonicMinor;
        showHarmonicMajor = harmonicMajor;
        showMelodicMinor = melodicMinor;
        _applyFilters();
      });
    });
  }

  /// Helper to determine if a header should be filtered
  bool _shouldIncludeHeader(String header) {
    if (header == 'Live keys') return true;

    if (header.contains('Harmonic Minor')) return showHarmonicMinor;
    if (header.contains('Harmonic Major')) return showHarmonicMajor;
    if (header.contains('Melodic Minor')) return showMelodicMinor;

    final majorPattern = RegExp(r'^[A-G][b#]?\sMajor');
    if (majorPattern.hasMatch(header)) return showMajor;

    return true; // default allow
  }

  /// Updates the legend with filtered suggestions
  void updateLegend(Map<String, Uint8List> suggestions) {
    latestSuggestions = suggestions; // cache for instant filter updates

    // Defer setState to avoid calling during build
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      _applyFilters();
    });
  }

  /// Apply current filter settings to the cached suggestions
  void _applyFilters() {
    // This function can be called safely here because we deferred via addPostFrameCallback
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
    setState(() {}); // rebuild with updated legend colors
  }

  /// Return only the filtered suggestion masks
  Map<String, Uint8List> get filteredSuggestionMasks {
    final Map<String, Uint8List> filtered = {};
    latestSuggestions.forEach((header, mask) {
      if (_shouldIncludeHeader(header)) {
        filtered[header] = mask;
      }
    });
    return filtered;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: null,
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
              onChanged: (val) async {
                final value = val ?? true;
                await _settingsService.setShowMajor(value);
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (!mounted) return;
                  setState(() {
                    showMajor = value;
                    _applyFilters();
                  });
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Harmonic Minor Scales"),
              value: showHarmonicMinor,
              onChanged: (val) async {
                final value = val ?? true;
                await _settingsService.setShowHarmonicMinor(value);
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (!mounted) return;
                  setState(() {
                    showHarmonicMinor = value;
                    _applyFilters();
                  });
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Harmonic Major Scales"),
              value: showHarmonicMajor,
              onChanged: (val) async {
                final value = val ?? true;
                await _settingsService.setShowHarmonicMajor(value);
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (!mounted) return;
                  setState(() {
                    showHarmonicMajor = value;
                    _applyFilters();
                  });
                });
              },
            ),
            CheckboxListTile(
              title: const Text("Melodic Minor Scales"),
              value: showMelodicMinor,
              onChanged: (val) async {
                final value = val ?? true;
                await _settingsService.setShowMelodicMinor(value);
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (!mounted) return;
                  setState(() {
                    showMelodicMinor = value;
                    _applyFilters();
                  });
                });
              },
            ),
          ],
        ),
      ),
      body: Stack(
        children: [
          // ScaleLegend with vertical stacking
          ScaleLegend(headerColors: legendColors, horizontalNudge: 100),

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
                  suggestionMasks: filteredSuggestionMasks,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
