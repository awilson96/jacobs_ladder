import 'package:flutter/material.dart';

/// Returns a consistent color for a given header string.
/// Both Page1 and PianoUdpController should import and use this.
Color colorForHeader(String header) {
  if (header.startsWith('A ')) return Colors.red;
  if (header.startsWith('Bb')) return Colors.deepOrange;
  if (header.startsWith('B ')) return Colors.orange;
  if (header.startsWith('C')) return Colors.yellow;
  if (header.startsWith('Db')) return Colors.lightGreen;
  if (header.startsWith('D ')) return Colors.green.shade800;
  if (header.startsWith('Eb')) return Colors.teal;
  if (header.startsWith('E ')) return Colors.lightBlue;
  if (header.startsWith('F')) return Colors.indigo;
  if (header.startsWith('Gb')) return Colors.purple.shade400;
  if (header.startsWith('G ')) return Colors.purple.shade900;
  if (header.startsWith('Ab')) return Colors.pink;

  // fallback if header doesn’t match
  return Colors.grey;
}

enum PianoColorMode {
  suggestionColoring, // default
  liveOnly,
  overlapHeatmap,
}
