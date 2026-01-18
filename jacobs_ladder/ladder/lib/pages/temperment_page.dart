import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../models/color_mapping.dart';
import '../widgets/piano.dart';
// import '../services/settings_service.dart';
import '../services/udp_service.dart';
import "../models/message_heap.dart";

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

  List<MessageHeap> liveHeap = [];


  @override
  void initState() {
    super.initState();
  }

  /// Returns a widget displaying the current live message heap as a table.
Widget _buildHeapTable() {
  if (liveHeap.isEmpty) {
    return const Center(
      child: Text("No messages received yet."),
    );
  }

  return SingleChildScrollView(
    scrollDirection: Axis.horizontal,
    child: DataTable(
      columns: const [
        DataColumn(label: Text('Note')),
        DataColumn(label: Text('Instance')),
        DataColumn(label: Text('Status')),
        DataColumn(label: Text('Velocity')),
        DataColumn(label: Text('Analog Abs')),
        DataColumn(label: Text('Analog Rel')),
        DataColumn(label: Text('Cents')),
        DataColumn(label: Text('Note Order')),
        DataColumn(label: Text('Ratio')),
        DataColumn(label: Text('Direction')),
      ],
      rows: liveHeap.map((msg) {
        final p = msg.pitchInfo;
        return DataRow(cells: [
          DataCell(Text(msg.midiNote.toString())),
          DataCell(Text(msg.instanceIndex.toString())),
          DataCell(Text(msg.status.toString())),
          DataCell(Text(msg.velocity.toString())),
          DataCell(Text(p.analogAbs.toString())),
          DataCell(Text(p.analogRel.toString())),
          DataCell(Text(p.cents.toStringAsFixed(2))),
          DataCell(Text(p.noteOrder.toString())),
          DataCell(Text(p.ratio)),
          DataCell(Text(p.direction)),
        ]);
      }).toList(),
    ),
  );
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
      body: Column(
        children: [
          // Debug table takes available vertical space above piano
          Expanded(
            child: _buildHeapTable(),
          ),

          // Fixed-height area for piano
          SizedBox(
            height: 300, // adjust as needed for your piano widget
            child: Center(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Piano(
                  udpService: widget.udpService,
                  suggestionMasks: activeSuggestionMasks,
                  colorMode: PianoColorMode.liveOnly,
                  showTuningInfo: true,
                  onHeapUpdate: (heap) {
                    setState(() {
                      liveHeap = heap;
                    });
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
