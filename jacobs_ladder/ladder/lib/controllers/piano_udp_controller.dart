// piano_udp_controller.dart
import 'dart:typed_data';
import 'dart:async';
import 'package:flutter/material.dart';

import '../models/color_mapping.dart';
import '../models/message_heap.dart';
import '../models/key_mapping.dart';
import '../services/udp_service.dart';

typedef KeyUpdateCallback = void Function(bool isWhite, int keyIndex, bool pressed);
typedef SuggestionUpdateCallback = void Function(Map<String, Uint8List> suggestions);
typedef KeyColorUpdateCallback = void Function(Map<int, Color> keyColors);

class PianoUdpController {
  final UdpService udpService;
  final KeyUpdateCallback onKeyUpdate;
  final SuggestionUpdateCallback? onSuggestionUpdate;
  final KeyColorUpdateCallback? onKeyColorUpdate;
  final void Function(List<MessageHeap>)? onHeapUpdate;

  StreamSubscription<Uint8List>? _udpSubscription;

  // Last Live keys mask
  List<int> _lastLiveMask = List.filled(11, 0);

  // All suggestion masks
  final Map<String, Uint8List> suggestionMasks = {};
  final PianoColorMode colorMode;
  final double lowThreshold;
  final double highThreshold;

  // Filter flags for different scale types
  bool showMajor = true;
  bool showHarmonicMinor = true;
  bool showHarmonicMajor = true;
  bool showMelodicMinor = true;

  // Temperment stuff
  List<MessageHeap> liveMessageHeap = [];

  PianoUdpController({
    required this.udpService,
    required this.onKeyUpdate,
    this.onSuggestionUpdate,
    this.onKeyColorUpdate,
    this.onHeapUpdate,
    this.showMajor = true,
    this.showHarmonicMinor = true,
    this.showHarmonicMajor = true,
    this.showMelodicMinor = true,
    this.colorMode = PianoColorMode.overlapHeatmap,
    this.lowThreshold = 0.33,
    this.highThreshold = 0.66,
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
    // Subscribe to the udpService
    _udpSubscription = udpService.messages.listen((data) {
      _handleIncomingMessage(data);
    });
  }

  void dispose() {
    _udpSubscription?.cancel();
  }


  void _handleIncomingMessage(Uint8List data) {
    int offset = 0;
    const int headerLength = 25;
    const int maskLength = 11;

    if (data.length < 4) {
      return;
    }

    // Read the 32-bit message type (big-endian)
    int messageType = (data[offset] << 24) |
        (data[offset + 1] << 16) |
        (data[offset + 2] << 8) |
        (data[offset + 3]);
    offset += 4;

    final Map<String, Uint8List> newSuggestionMasks = {};

    // If the message type is keys and bitmasks for updating the piano widget
    if (messageType == 1) {
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
    // Message type of message_heap 
    else if (messageType == 2) {
      List<MessageHeap> heap = [];

      const int entrySize = 25;

      while (offset + entrySize <= data.length) {
        int midiNote = data[offset];
        int instanceIndex = data[offset + 1];
        int status = data[offset + 2];
        int velocity = data[offset + 3];
        offset += 4;

        int analogAbs =
            (data[offset] << 8) | data[offset + 1];
        int analogRel =
            (data[offset + 2] << 8) | data[offset + 3];
        if (analogRel & 0x8000 != 0) {
          analogRel -= 0x10000; // signed short
        }

        ByteData bd = ByteData(4);
        for (int i = 0; i < 4; i++) {
          bd.setUint8(i, data[offset + 4 + i]);
        }
        double cents = bd.getFloat32(0, Endian.big);

        int noteOrder =
            (data[offset + 8] << 8) | data[offset + 9];
        if (noteOrder & 0x8000 != 0) {
          noteOrder -= 0x10000;
        }

        String ratio = String.fromCharCodes(
          data.sublist(offset + 10, offset + 20),
        ).trim();

        int dirByte = data[offset + 20];
        String direction = switch (dirByte) {
          117 => "up",    // 'u'
          100 => "down",  // 'd'
          _ => "none",    // 'n'
        };

        offset += 21;

        PitchInfo pitchInfo = PitchInfo(
          analogAbs: analogAbs,
          analogRel: analogRel,
          cents: cents,
          noteOrder: noteOrder,
          ratio: ratio,
          direction: direction,
        );

        heap.add(MessageHeap(
          midiNote: midiNote,
          instanceIndex: instanceIndex,
          status: status,
          velocity: velocity,
          pitchInfo: pitchInfo,
        ));
      }

      liveMessageHeap = heap;
      onHeapUpdate?.call(heap);
    }
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

    switch (colorMode) {
      case PianoColorMode.liveOnly:
        _updateLiveOnlyColors();
        break;
      case PianoColorMode.overlapHeatmap:
        _updateHeatmapColors();
        break;
      case PianoColorMode.suggestionColoring:
        _updatePerScaleColors();
        break;
    }
  }

  void _updateLiveOnlyColors() {
    Map<int, Color> colorMask = {};

    int encodeKey(bool isWhite, int keyIndex) => isWhite ? keyIndex : keyIndex + 100;

    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int byte = _lastLiveMask[byteIndex];
      for (int bit = 0; bit < 8; bit++) {
        int linearIndex = byteIndex * 8 + bit;
        if (linearIndex >= bitToKeyMap.length) continue;
        if ((byte & (1 << bit)) != 0) {
          final mapping = bitToKeyMap[linearIndex];
          int key = encodeKey(mapping.key, mapping.value);
          colorMask[key] = Colors.green; // or sky blue, depending on mode
        }
      }
    }

    onKeyColorUpdate!(colorMask);
  }

  void _updatePerScaleColors() {
    if (onKeyColorUpdate == null) return;

    Map<int, Color> finalColorMask = {};
    Set<int> skipKeys = {};
    Set<int> visitedKeys = {};

    int encodeKey(bool isWhite, int keyIndex) => isWhite ? keyIndex : keyIndex + 100;

    // --- Live keys are now green ---
    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int byte = _lastLiveMask[byteIndex];
      for (int bit = 0; bit < 8; bit++) {
        int linearIndex = byteIndex * 8 + bit;
        if (linearIndex >= bitToKeyMap.length) continue;
        if ((byte & (1 << bit)) != 0) {
          final mapping = bitToKeyMap[linearIndex];
          int key = encodeKey(mapping.key, mapping.value);
          finalColorMask[key] = Colors.green;
          skipKeys.add(key);
        }
      }
    }

    // --- Suggestion masks colored by header first letter ---
    for (var entry in suggestionMasks.entries) {
      String header = entry.key;
      Uint8List mask = entry.value;
      if (header == 'Live keys') continue;
      Color color = colorForHeader(header);

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

  void _updateHeatmapColors() {
    Map<int, int> overlapCount = {};
    Map<int, Color> finalColors = {};

    int encodeKey(bool isWhite, int keyIndex) => isWhite ? keyIndex : keyIndex + 100;

    // Count how many suggestion masks have each key on
    for (var entry in suggestionMasks.entries) {
      String header = entry.key;
      if (header == 'Live keys') continue;
      Uint8List mask = entry.value;

      for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
        int byte = mask[byteIndex];
        for (int bit = 0; bit < 8; bit++) {
          int linearIndex = byteIndex * 8 + bit;
          if (linearIndex >= bitToKeyMap.length) continue;
          if ((byte & (1 << bit)) != 0) {
            final mapping = bitToKeyMap[linearIndex];
            int key = encodeKey(mapping.key, mapping.value);
            overlapCount[key] = (overlapCount[key] ?? 0) + 1;
          }
        }
      }
    }

    // Compute thresholds
    if (overlapCount.isEmpty) {
      onKeyColorUpdate!({});
      return;
    }

    int maxOverlap = overlapCount.values.fold(0, (a, b) => a > b ? a : b);

    // Color keys by relative overlap
    overlapCount.forEach((key, count) {
      double ratio = count / maxOverlap;

      if (ratio >= highThreshold) {
        finalColors[key] = Colors.green;
      } else if (ratio >= lowThreshold) {
        finalColors[key] = Colors.yellow;
      } else if (ratio > 0) {
        finalColors[key] = Colors.red;
      }
    });

    // Add live keys (always sky blue)
    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int byte = _lastLiveMask[byteIndex];
      for (int bit = 0; bit < 8; bit++) {
        int linearIndex = byteIndex * 8 + bit;
        if (linearIndex >= bitToKeyMap.length) continue;
        if ((byte & (1 << bit)) != 0) {
          final mapping = bitToKeyMap[linearIndex];
          int key = encodeKey(mapping.key, mapping.value);
          finalColors[key] = Colors.lightBlue;
        }
      }
    }

    onKeyColorUpdate!(finalColors);
  }
}
