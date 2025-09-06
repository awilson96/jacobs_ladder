import 'package:shared_preferences/shared_preferences.dart';
import '../models/app_theme.dart';

class SettingsService {
  static const _themeKey = 'app_theme';

  Future<AppTheme> loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    final savedTheme = prefs.getString(_themeKey);

    if (savedTheme != null) {
      return AppTheme.values.firstWhere(
        (t) => t.toString() == savedTheme,
        orElse: () => AppTheme.dark,
      );
    }
    return AppTheme.dark; // default
  }

  Future<void> saveTheme(AppTheme theme) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_themeKey, theme.toString());
  }
}
