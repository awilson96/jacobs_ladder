import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/app_theme.dart';
import '../services/udp_service.dart';
import 'dart:typed_data';
import 'dart:async';

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

  @override
  void initState() {
    super.initState();
    _selectedTheme = widget.currentTheme;
    _loadTheme();

    // Subscribe to UDP messages
    _udpSubscription = widget.udpService.messages.listen((data) {
      _handleUdpMessage(data);
    });
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
    // Example: handle incoming messages if needed
    // You can decode and respond here
    // For now, just print:
    debugPrint('SettingsPage received UDP message: $data');
  }

  void _sendUdpMessage(Uint8List data) {
    widget.udpService.send(data);
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
        child: Align(
          alignment: Alignment.topCenter,
          child: Row(
            mainAxisSize: MainAxisSize.min,
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
                    _saveTheme(value); // persist selection
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
