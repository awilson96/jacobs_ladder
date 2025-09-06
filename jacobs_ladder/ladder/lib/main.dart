import 'package:flutter/material.dart';
import 'app.dart';
import 'controllers/settings_controller.dart';
import 'services/settings_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final settingsController = SettingsController(SettingsService());
  await settingsController.loadSettings();

  runApp(LadderApp(settingsController: settingsController));
}
