import 'package:flutter/foundation.dart';
import '../models/app_theme.dart';
import '../services/settings_service.dart';

class SettingsController extends ChangeNotifier {
  SettingsController(this._settingsService);

  final SettingsService _settingsService;

  late AppTheme _theme;
  AppTheme get theme => _theme;

  Future<void> loadSettings() async {
    _theme = await _settingsService.loadTheme();
    notifyListeners();
  }

  Future<void> updateTheme(AppTheme newTheme) async {
    if (newTheme == _theme) return;
    _theme = newTheme;
    notifyListeners();
    await _settingsService.saveTheme(newTheme);
  }
}
