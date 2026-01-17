import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../models/color_mapping.dart';
import '../widgets/piano.dart';
// import '../services/settings_service.dart';
import '../services/udp_service.dart';

/// TempermentPage with Piano, vertical stacked legend, and persistent settings
class TempermentPage extends StatefulWidget {
  const TempermentPage({super.key, required this.udpService});

  final UdpService udpService;

  @override
  State<TempermentPage> createState() => _TempermentPageState();
}

class _TempermentPageState extends State<TempermentPage> {
  // Map of header -> Color (Live keys always green now)
  Map<String, Color> legendColors = {'Live keys': Colors.green};


  // Keep latest suggestions so we can re-filter instantly
  Map<String, Uint8List> latestSuggestions = {};

  // Currently selected scale for filtering (null = no filter)
  String? selectedHeader;

  // final SettingsService _settingsService = SettingsService();
  Map<String, Uint8List> get activeSuggestionMasks => latestSuggestions;


  @override
  void initState() {
    super.initState();
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
          ],
        ),
      ),
      body: Stack(
        children: [
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Center(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Piano(
                  udpService: widget.udpService,
                  suggestionMasks: activeSuggestionMasks,
                  colorMode: PianoColorMode.liveOnly,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
