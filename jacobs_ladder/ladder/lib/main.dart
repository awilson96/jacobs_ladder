// System imports
import 'dart:developer' as dev;
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:window_size/window_size.dart' as window_size;
import 'package:flutter/foundation.dart';

// Local imports
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (!kIsWeb && (Platform.isWindows || Platform.isLinux || Platform.isMacOS)) {
    dev.log("Desktop Application was selected");
    final screens = await window_size.getScreenList();
    if (screens.isNotEmpty) {
      final screen = screens.first;
      final screenWidth = screen.frame.width;

      // Set min size to 50% of screen width, keep your height min
      final minWidth = screenWidth * 0.5;
      const minHeight = 350.0;

      window_size.setWindowMinSize(Size(minWidth, minHeight));
    } else {
      // fallback if no screen info
      window_size.setWindowMinSize(const Size(400, 350));
    }
  } else {
      dev.log("Web application was selected.");
  }

  runApp(const LadderApp());
}
