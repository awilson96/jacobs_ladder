import 'package:flutter/material.dart';
import 'models/app_theme.dart';
import 'pages/home_page.dart';

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
