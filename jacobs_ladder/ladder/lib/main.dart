import 'package:flutter/material.dart';

void main() {
  runApp(const LadderApp());
}

enum AppTheme { light, dark }

class LadderApp extends StatefulWidget {
  const LadderApp({super.key});

  @override
  State<LadderApp> createState() => _LadderAppState();
}

class _LadderAppState extends State<LadderApp> {
  AppTheme _currentTheme = AppTheme.dark;

  void _updateTheme(AppTheme newTheme) {
    setState(() {
      _currentTheme = newTheme;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ladder',
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: _currentTheme == AppTheme.dark ? ThemeMode.dark : ThemeMode.light,
      home: HomePage(
        title: 'Ladder',
        currentTheme: _currentTheme,
        updateTheme: _updateTheme,
      ),
    );
  }
}

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

  final List<Widget> _pages = [
    const Page1(),
    const Page2(),
  ];

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
            const DrawerHeader(
              decoration: BoxDecoration(color: Colors.deepPurple),
              child: Text('Ladder Menu',
                  style: TextStyle(color: Colors.white, fontSize: 24)),
            ),
            ListTile(
              leading: const Icon(Icons.looks_one),
              title: const Text('Page 1'),
              selected: _selectedIndex == 0,
              onTap: () => _selectPage(0),
            ),
            ListTile(
              leading: const Icon(Icons.looks_two),
              title: const Text('Page 2'),
              selected: _selectedIndex == 1,
              onTap: () => _selectPage(1),
            ),
            const Spacer(),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Settings'),
              onTap: () {
                Navigator.of(context).pop(); // close drawer first
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => SettingsPage(
                    currentTheme: widget.currentTheme,
                    updateTheme: widget.updateTheme,
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

// ------------------- Pages -------------------

class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Page 1', style: TextStyle(fontSize: 32)),
    );
  }
}

class Page2 extends StatelessWidget {
  const Page2({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Page 2', style: TextStyle(fontSize: 32)),
    );
  }
}

// ------------------- Settings Page -------------------

class SettingsPage extends StatefulWidget {
  const SettingsPage({
    super.key,
    required this.currentTheme,
    required this.updateTheme,
  });

  final AppTheme currentTheme;
  final Function(AppTheme) updateTheme;

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  late AppTheme _selectedTheme;

  @override
  void initState() {
    super.initState();
    _selectedTheme = widget.currentTheme;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: Padding(
        padding: const EdgeInsets.only(top: 20.0), // smaller padding from top
        child: Align(
          alignment: Alignment.topCenter, // horizontally center and top vertical
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Theme:',
                style: TextStyle(fontSize: 20),
              ),
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
                    widget.updateTheme(value); // immediately update theme
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

