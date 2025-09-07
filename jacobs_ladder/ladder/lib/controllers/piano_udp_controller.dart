// piano_udp_controller.dart
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

  PianoUdpController({
    required this.onKeyUpdate,
    this.onSuggestionUpdate,
    this.onKeyColorUpdate,
  });

  Future<void> start() async {
    _socket = await RawDatagramSocket.bind(InternetAddress.loopbackIPv4, 50000);
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
      } else {
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
    Set<int> skipKeys = {};  // Live keys or overlapping notes
    Set<int> visitedKeys = {};

    // Helper to encode key index with isWhite
    int encodeKey(bool isWhite, int keyIndex) => isWhite ? keyIndex : keyIndex + 100;

    // First, mark live keys red
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

    // Now process all suggestion masks
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
