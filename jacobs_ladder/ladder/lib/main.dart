import 'package:flutter/material.dart';

void main() {
  runApp(const LadderApp());
}

class LadderApp extends StatelessWidget {
  const LadderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ladder',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const HomePage(title: 'Ladder'),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;

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
    Navigator.of(context).pop(); // Close the drawer after selection
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.deepPurple,
              ),
              child: Text(
                'Ladder Menu',
                style: TextStyle(color: Colors.white, fontSize: 24),
              ),
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
          ],
        ),
      ),
      body: _pages[_selectedIndex],
    );
  }
}

// Page 1 placeholder
class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'Page 1',
        style: TextStyle(fontSize: 32),
      ),
    );
  }
}

// Page 2 placeholder
class Page2 extends StatelessWidget {
  const Page2({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'Page 2',
        style: TextStyle(fontSize: 32),
      ),
    );
  }
}
