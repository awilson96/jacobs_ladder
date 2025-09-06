import 'package:flutter/material.dart';
import 'controllers/settings_controller.dart';
import 'services/settings_service.dart';
import 'models/app_theme.dart';
import 'pages/home_page.dart';

class LadderApp extends StatelessWidget {
  const LadderApp({super.key, required this.settingsController});

  final SettingsController settingsController;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: settingsController,
      builder: (context, _) {
        return MaterialApp(
          title: 'Ladder',
          theme: ThemeData.light(),
          darkTheme: ThemeData.dark(),
          themeMode: settingsController.theme == AppTheme.dark
              ? ThemeMode.dark
              : ThemeMode.light,
          home: HomePage(
            title: 'Ladder',
            currentTheme: settingsController.theme,
            updateTheme: settingsController.updateTheme,
          ),
        );
      },
    );
  }
}
