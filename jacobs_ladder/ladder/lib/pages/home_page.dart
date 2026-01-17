import 'package:flutter/material.dart';

import '../models/app_theme.dart';
import 'page1.dart';
import 'page2.dart';
import 'temperment_page.dart';
import 'page3.dart';
import 'settings_page.dart';
import '../services/udp_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({
    super.key,
    required this.title,
    required this.currentTheme,
    required this.updateTheme,
  });

  final String title;
  final AppTheme currentTheme;
  final Function(AppTheme) updateTheme;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;
  late final UdpService udpService;
  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();

    // Instantiate the UDP service
    udpService = UdpService();
    udpService.start();

    // Initialize pages after udpService is available
    _pages = [
      Page1(udpService: udpService),
      Page2(udpService: udpService),
      TempermentPage(udpService: udpService),
      Page3(udpService: udpService),
    ];
  }

  @override
  void dispose() {
    udpService.stop();
    super.dispose();
  }

  void _selectPage(int index) {
    setState(() {
      _selectedIndex = index;
    });
    Navigator.of(context).pop(); // close drawer
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      drawer: Drawer(
        child: Column(
          children: [
            Container(
              height: 56,
              width: double.infinity,
              color: const Color.fromARGB(255, 52, 64, 52),
              alignment: Alignment.center,
              child: const Text(
                'Menu',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.music_note),
              title: const Text('Scale Explorer'),
              selected: _selectedIndex == 0,
              onTap: () => _selectPage(0),
            ),
            ListTile(
              leading: const Icon(Icons.storage),
              title: const Text('Lick Database'),
              selected: _selectedIndex == 1,
              onTap: () => _selectPage(1),
            ),
            ListTile(
              leading: const Icon(Icons.tune),
              title: const Text('Temperament Explorer'),
              selected: _selectedIndex == 2,
              onTap: () => _selectPage(2),
            ),
            ListTile(
              leading: const Icon(Icons.mic),
              title: const Text('Midi Recorder'),
              selected: _selectedIndex == 3,
              onTap: () => _selectPage(3),
            ),
            const Spacer(),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Settings'),
              onTap: () {
                Navigator.of(context).pop();
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => SettingsPage(
                    currentTheme: widget.currentTheme,
                    updateTheme: widget.updateTheme,
                    udpService: udpService, // pass UDP service
                  ),
                ));
              },
            ),
          ],
        ),
      ),
      body: _pages[_selectedIndex],
    );
  }
}
