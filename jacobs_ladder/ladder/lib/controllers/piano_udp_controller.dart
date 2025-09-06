import 'dart:io';
import 'dart:typed_data';

import '../models/key_mapping.dart';

typedef KeyUpdateCallback = void Function(bool isWhite, int keyIndex, bool pressed);

class PianoUdpController {
  final KeyUpdateCallback onKeyUpdate;
  RawDatagramSocket? _socket;
  List<int> _lastMessage = List.filled(11, 0);

  PianoUdpController({required this.onKeyUpdate});

  /// Start listening for UDP messages
  Future<void> start() async {
    _socket = await RawDatagramSocket.bind(InternetAddress.loopbackIPv4, 50000);
    _socket!.listen((event) {
      if (event == RawSocketEvent.read) {
        Datagram? datagram = _socket!.receive();
        if (datagram != null && datagram.data.length == 11) {
          _handleIncomingMessage(datagram.data);
        }
      }
    });
  }

  void dispose() {
    _socket?.close();
  }

  void _handleIncomingMessage(Uint8List data) {
    for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
      int newByte = data[byteIndex];
      int oldByte = _lastMessage[byteIndex];

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

    _lastMessage = List<int>.from(data);
  }
}
