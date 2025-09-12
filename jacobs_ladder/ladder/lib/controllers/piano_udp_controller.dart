import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';

import '../models/key_mapping.dart';

typedef KeyUpdateCallback = void Function(bool isWhite, int keyIndex, bool pressed);
typedef SuggestionUpdateCallback = void Function(Map<String, Uint8List> suggestions);
typedef KeyColorUpdateCallback = void Function(Map<int, Color> keyColors);

class PianoUdpController {
  final KeyUpdateCallback onKeyUpdate;
  final SuggestionUpdateCallback? onSuggestionUpdate;
  final KeyColorUpdateCallback? onKeyColorUpdate;

  RawDatagramSocket? _socket;

  // Last Live keys mask
  List<int> _lastLiveMask = List.filled(11, 0);

  // All suggestion masks
  final Map<String, Uint8List> suggestionMasks = {};

  // Colors for suggestions
  final List<Color> suggestionColors = [
    Colors.orange,
    Colors.yellow,
    Colors.green,
    Colors.teal,
    Colors.blue,
    Colors.purple,
    Colors.pink,
  ];

  // Filter flags for different scale types
  bool showMajor = true;
  bool showHarmonicMinor = true;
  bool showHarmonicMajor = true;
  bool showMelodicMinor = true;

  PianoUdpController({
    required this.onKeyUpdate,
    this.onSuggestionUpdate,
    this.onKeyColorUpdate,
    this.showMajor = true,
    this.showHarmonicMinor = true,
    this.showHarmonicMajor = true,
    this.showMelodicMinor = true,
  });

  /// Static function for header filtering
  static bool shouldIncludeHeader(
    String header, {
    required bool showMajor,
    required bool showHarmonicMinor,
    required bool showHarmonicMajor,
    required bool showMelodicMinor,
  }) {
    if (header == 'Live keys') return true;
    if (header.contains('Harmonic Minor')) return showHarmonicMinor;
    if (header.contains('Harmonic Major')) return showHarmonicMajor;
    if (header.contains('Melodic Minor')) return showMelodicMinor;

    final majorPattern = RegExp(r'^[A-G][b#]?\sMajor');
    if (majorPattern.hasMatch(header)) return showMajor;

    return true;
  }

  /// Update filter flags dynamically
  void updateFilters({
    bool? major,
    bool? harmonicMinor,
    bool? harmonicMajor,
    bool? melodicMinor,
  }) {
    if (major != null) showMajor = major;
    if (harmonicMinor != null) showHarmonicMinor = harmonicMinor;
    if (harmonicMajor != null) showHarmonicMajor = harmonicMajor;
    if (melodicMinor != null) showMelodicMinor = melodicMinor;
  }

  /// Set suggestion masks from external source (e.g., Page1) and update colors
  void setSuggestionMasks(Map<String, Uint8List> masks) {
    suggestionMasks
      ..clear()
      ..addAll(masks);

    if (onSuggestionUpdate != null) {
      onSuggestionUpdate!(Map<String, Uint8List>.from(suggestionMasks));
    }

    _updateSuggestionColors();
  }

  Future<void> start() async {
    _socket = await RawDatagramSocket.bind(InternetAddress.loopbackIPv4, 50005);
    _socket!.listen((event) {
      if (event == RawSocketEvent.read) {
        Datagram? datagram = _socket!.receive();
        if (datagram != null) {
          _handleIncomingMessage(datagram.data);
        }
      }
    });
  }

  void dispose() {
    _socket?.close();
  }

  void _handleIncomingMessage(Uint8List data) {
    int offset = 0;
    const int headerLength = 25;
    const int maskLength = 11;

    final Map<String, Uint8List> newSuggestionMasks = {};

    while (offset + headerLength + maskLength <= data.length) {
      String header = String.fromCharCodes(
        data.sublist(offset, offset + headerLength),
      ).trim();
      offset += headerLength;

      Uint8List mask = data.sublist(offset, offset + maskLength);
      offset += maskLength;

      if (header == 'Live keys') {
        _updateLiveKeys(mask);
      } else if (shouldIncludeHeader(
        header,
        showMajor: showMajor,
        showHarmonicMinor: showHarmonicMinor,
        showHarmonicMajor: showHarmonicMajor,
        showMelodicMinor: showMelodicMinor,
      )) {
        newSuggestionMasks[header] = mask;
      }
    }

    suggestionMasks
      ..clear()
      ..addAll(newSuggestionMasks);

    if (onSuggestionUpdate != null) {
      onSuggestionUpdate!(Map<String, Uint8List>.from(suggestionMasks));
    }

    _updateSuggestionColors();
  }

  void _updateLiveKeys(Uint8List mask) {
    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int newByte = mask[byteIndex];
      int oldByte = _lastLiveMask[byteIndex];

      for (int bit = 0; bit < 8; bit++) {
        int linearIndex = byteIndex * 8 + bit;
        if (linearIndex >= bitToKeyMap.length) continue;

        bool oldOn = (oldByte & (1 << bit)) != 0;
        bool newOn = (newByte & (1 << bit)) != 0;

        if (oldOn != newOn) {
          final mapping = bitToKeyMap[linearIndex];
          onKeyUpdate(mapping.key, mapping.value, newOn);
        }
      }
    }
    _lastLiveMask = List<int>.from(mask);
  }

  void _updateSuggestionColors() {
    if (onKeyColorUpdate == null) return;

    Map<int, Color> finalColorMask = {};
    Set<int> skipKeys = {};
    Set<int> visitedKeys = {};

    int encodeKey(bool isWhite, int keyIndex) => isWhite ? keyIndex : keyIndex + 100;

    // Mark live keys red
    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int byte = _lastLiveMask[byteIndex];
      for (int bit = 0; bit < 8; bit++) {
        int linearIndex = byteIndex * 8 + bit;
        if (linearIndex >= bitToKeyMap.length) continue;
        if ((byte & (1 << bit)) != 0) {
          final mapping = bitToKeyMap[linearIndex];
          int key = encodeKey(mapping.key, mapping.value);
          finalColorMask[key] = Colors.red;
          skipKeys.add(key);
        }
      }
    }

    // Process suggestion masks
    int colorIndex = 0;
    for (var mask in suggestionMasks.values) {
      Color color = suggestionColors[colorIndex % suggestionColors.length];
      colorIndex++;

      for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
        int byte = mask[byteIndex];
        for (int bit = 0; bit < 8; bit++) {
          int linearIndex = byteIndex * 8 + bit;
          if (linearIndex >= bitToKeyMap.length) continue;
          if ((byte & (1 << bit)) != 0) {
            final mapping = bitToKeyMap[linearIndex];
            int key = encodeKey(mapping.key, mapping.value);

            if (skipKeys.contains(key)) continue;

            if (visitedKeys.contains(key)) {
              finalColorMask[key] = Colors.grey;
              skipKeys.add(key);
            } else {
              finalColorMask[key] = color;
              visitedKeys.add(key);
            }
          }
        }
      }
    }

    onKeyColorUpdate!(finalColorMask);
  }
}
