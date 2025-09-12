import 'package:flutter/material.dart';
import '../services/settings_service.dart';

class ScaleFilterDrawer extends StatefulWidget {
  final bool showMajor;
  final bool showHarmonicMinor;
  final bool showHarmonicMajor;
  final bool showMelodicMinor;
  final SettingsService settingsService;
  final Function(bool, bool, bool, bool) onFilterChanged;

  const ScaleFilterDrawer({
    super.key,
    required this.showMajor,
    required this.showHarmonicMinor,
    required this.showHarmonicMajor,
    required this.showMelodicMinor,
    required this.settingsService,
    required this.onFilterChanged,
  });

  @override
  State<ScaleFilterDrawer> createState() => _ScaleFilterDrawerState();
}

class _ScaleFilterDrawerState extends State<ScaleFilterDrawer> {
  late bool showMajor;
  late bool showHarmonicMinor;
  late bool showHarmonicMajor;
  late bool showMelodicMinor;

  @override
  void initState() {
    super.initState();
    showMajor = widget.showMajor;
    showHarmonicMinor = widget.showHarmonicMinor;
    showHarmonicMajor = widget.showHarmonicMajor;
    showMelodicMinor = widget.showMelodicMinor;
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const Text(
            "Scale Filters",
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const Divider(),
          _buildCheckbox("Major Scales", showMajor, (val) async {
            showMajor = val ?? true;
            await widget.settingsService.setShowMajor(showMajor);
            widget.onFilterChanged(showMajor, showHarmonicMinor, showHarmonicMajor, showMelodicMinor);
            setState(() {});
          }),
          _buildCheckbox("Harmonic Minor Scales", showHarmonicMinor, (val) async {
            showHarmonicMinor = val ?? true;
            await widget.settingsService.setShowHarmonicMinor(showHarmonicMinor);
            widget.onFilterChanged(showMajor, showHarmonicMinor, showHarmonicMajor, showMelodicMinor);
            setState(() {});
          }),
          _buildCheckbox("Harmonic Major Scales", showHarmonicMajor, (val) async {
            showHarmonicMajor = val ?? true;
            await widget.settingsService.setShowHarmonicMajor(showHarmonicMajor);
            widget.onFilterChanged(showMajor, showHarmonicMinor, showHarmonicMajor, showMelodicMinor);
            setState(() {});
          }),
          _buildCheckbox("Melodic Minor Scales", showMelodicMinor, (val) async {
            showMelodicMinor = val ?? true;
            await widget.settingsService.setShowMelodicMinor(showMelodicMinor);
            widget.onFilterChanged(showMajor, showHarmonicMinor, showHarmonicMajor, showMelodicMinor);
            setState(() {});
          }),
        ],
      ),
    );
  }

  Widget _buildCheckbox(String title, bool value, ValueChanged<bool?> onChanged) {
    return CheckboxListTile(title: Text(title), value: value, onChanged: onChanged);
  }
}
