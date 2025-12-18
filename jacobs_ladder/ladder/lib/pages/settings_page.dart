import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/app_theme.dart';
import '../services/udp_service.dart';
import 'dart:typed_data';
import 'dart:async';
import 'dart:convert';

class SettingsPage extends StatefulWidget {
  const SettingsPage({
    super.key,
    required this.currentTheme,
    required this.updateTheme,
    required this.udpService,
  });

  final AppTheme currentTheme;
  final Function(AppTheme) updateTheme;
  final UdpService udpService;

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  late AppTheme _selectedTheme;
  StreamSubscription<Uint8List>? _udpSubscription;

  // MIDI port handling
  List<String> _midiPorts = [];
  String? _selectedMidiPort;

  @override
  void initState() {
    super.initState();
    _selectedTheme = widget.currentTheme;
    _loadTheme();

    // Subscribe to UDP messages
    _udpSubscription = widget.udpService.messages.listen((data) {
      _handleUdpMessage(data);
    });

    // Request MIDI ports from Python backend
    _requestMidiPorts();
  }

  Future<void> _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    final savedTheme = prefs.getString('app_theme');
    if (savedTheme != null) {
      setState(() {
        _selectedTheme = AppTheme.values
            .firstWhere((t) => t.toString() == savedTheme, orElse: () => widget.currentTheme);
      });
      widget.updateTheme(_selectedTheme);
    }
  }

  Future<void> _saveTheme(AppTheme theme) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('app_theme', theme.toString());
  }

  void _handleUdpMessage(Uint8List data) {
    if (data.length < 4) return;

    // First 4 bytes are the message type (big-endian)
    final messageType = data.buffer.asByteData().getUint32(0);
    final payload = data.sublist(4);

    if (messageType == 2) {
      // MIDI ports list
      final text = utf8.decode(payload, allowMalformed: true);
      final ports = text.split('\x00').where((s) => s.isNotEmpty).toList();
      setState(() {
        _midiPorts = ports;
        if (_selectedMidiPort == null && ports.isNotEmpty) {
          _selectedMidiPort = ports.first;
        }
      });
    }
  }

  void _requestMidiPorts() {
    // Type 2 message with empty payload
    final message = Uint8List(4);
    final byteData = message.buffer.asByteData();
    byteData.setUint32(0, 2); // message type 2
    widget.udpService.send(message);
  }

  void _sendSelectedMidiPort(String port) {
    // Send message type 3 with port as UTF-8 payload
    final portBytes = utf8.encode(port);
    final message = Uint8List(4 + portBytes.length);
    final byteData = message.buffer.asByteData();
    byteData.setUint32(0, 3); // message type 3
    message.setAll(4, portBytes);
    widget.udpService.send(message);
  }

  @override
  void dispose() {
    _udpSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: Padding(
        padding: const EdgeInsets.only(top: 20.0),
        child: Column(
          children: [
            // Theme selection
            Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('Theme:', style: TextStyle(fontSize: 20)),
                const SizedBox(width: 10),
                DropdownButton<AppTheme>(
                  value: _selectedTheme,
                  items: const [
                    DropdownMenuItem(
                      value: AppTheme.light,
                      child: Text('Light'),
                    ),
                    DropdownMenuItem(
                      value: AppTheme.dark,
                      child: Text('Dark'),
                    ),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() {
                        _selectedTheme = value;
                      });
                      widget.updateTheme(value);
                      _saveTheme(value);
                    }
                  },
                ),
              ],
            ),
            const SizedBox(height: 30),
            // MIDI input selection
            Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('MIDI Input:', style: TextStyle(fontSize: 20)),
                const SizedBox(width: 10),
                DropdownButton<String>(
                  value: _selectedMidiPort,
                  items: _midiPorts
                      .map((port) => DropdownMenuItem(
                            value: port,
                            child: Text(port),
                          ))
                      .toList(),
                  hint: const Text('Select MIDI Input'),
                  onChanged: (value) {
                    if (value == null) return;
                    setState(() {
                      _selectedMidiPort = value;
                    });
                    debugPrint('Selected MIDI port: $value');
                    _sendSelectedMidiPort(value); // send to backend
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
