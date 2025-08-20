import 'dart:io';
import 'package:flutter/material.dart';
import 'app.dart';
import 'package:window_size/window_size.dart' as window_size;

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    window_size.setWindowMinSize(const Size(400, 350));

  }
  runApp(const LadderApp());
}
