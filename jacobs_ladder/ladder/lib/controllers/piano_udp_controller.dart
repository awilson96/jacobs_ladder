import 'dart:io';
import 'dart:typed_data';

import '../models/key_mapping.dart';

typedef KeyUpdateCallback = void Function(bool isWhite, int keyIndex, bool pressed);

class PianoUdpController {
  final KeyUpdateCallback onKeyUpdate;
  RawDatagramSocket? _socket;

  // Store the last mask for LIVE_KEYS (yellow)
  List<int> _lastLiveMask = List.filled(11, 0);

  // Store all suggestion masks (header -> 11-byte mask)
  final Map<String, Uint8List> suggestionMasks = {};

  PianoUdpController({required this.onKeyUpdate});

  /// Start listening for UDP messages
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

  /// Handles incoming message with structure: [25 chars][11 bytes], repeated
  void _handleIncomingMessage(Uint8List data) {
    int offset = 0;
    const int headerLength = 25;
    const int maskLength = 11;

    while (offset + headerLength + maskLength <= data.length) {
      // Extract header
      String header = String.fromCharCodes(
        data.sublist(offset, offset + headerLength),
      ).trim();
      offset += headerLength;

      // Extract 11-byte mask
      Uint8List mask = data.sublist(offset, offset + maskLength);
      offset += maskLength;

      if (header == 'LIVE_KEYS') {
        // Update yellow keys
        _updateLiveKeys(mask);
      } else {
        // Store suggestion masks for later
        suggestionMasks[header] = mask;
      }
    }
  }

  /// Updates the yellow keys (LIVE_KEYS) based on incoming mask
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
}
