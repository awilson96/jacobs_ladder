import 'package:shared_preferences/shared_preferences.dart';
import '../models/app_theme.dart';

class SettingsService {
  static const _themeKey = 'app_theme';

  // New keys for scale filters
  static const _showMajorKey = 'show_major';
  static const _showHarmonicMinorKey = 'show_harmonic_minor';
  static const _showHarmonicMajorKey = 'show_harmonic_major';
  static const _showMelodicMinorKey = 'show_melodic_minor';

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

  /// Scale filter getters
  Future<bool> getShowMajor() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_showMajorKey) ?? true;
  }

  Future<bool> getShowHarmonicMinor() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_showHarmonicMinorKey) ?? true;
  }

  Future<bool> getShowHarmonicMajor() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_showHarmonicMajorKey) ?? true;
  }

  Future<bool> getShowMelodicMinor() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_showMelodicMinorKey) ?? true;
  }

  /// Scale filter setters
  Future<void> setShowMajor(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_showMajorKey, value);
  }

  Future<void> setShowHarmonicMinor(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_showHarmonicMinorKey, value);
  }

  Future<void> setShowHarmonicMajor(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_showHarmonicMajorKey, value);
  }

  Future<void> setShowMelodicMinor(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_showMelodicMinorKey, value);
  }
}
