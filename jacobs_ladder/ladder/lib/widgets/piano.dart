import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';

import '../models/key_mapping.dart';

class Piano extends StatefulWidget {
  const Piano({super.key});

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};

  // UDP variables
  RawDatagramSocket? _socket;
  List<int> _lastMessage = List.filled(11, 0); // Previous 11-byte state

  // Ratios for black keys relative to white keys
  static const double blackKeyHeightRatio = 0.65;
  static const double blackKeyWidthRatio = 0.6;

  // Piano keys — **keep your original array exactly**
  final List<String> whiteKeys = [
    'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'A', 'B',
    'C'
  ];

  final Map<String, bool> blackKeyPattern = {'C': true, 'D': true, 'F': true, 'G': true, 'A': true};

  @override
  void initState() {
    super.initState();
    _startUdpListener();
  }

  @override
  void dispose() {
    _socket?.close();
    super.dispose();
  }

  /// UDP listener setup on localhost
  void _startUdpListener() async {
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

  /// Handle incoming 11-byte message using bitToKeyMap
  void _handleIncomingMessage(Uint8List data) {
    setState(() {
      for (int byteIndex = 0; byteIndex < 11; byteIndex++) {
        int newByte = data[byteIndex];
        int oldByte = _lastMessage[byteIndex];

        for (int bit = 0; bit < 8; bit++) {
          int linearIndex = byteIndex * 8 + bit;

          if (linearIndex >= bitToKeyMap.length) continue; // ignore out-of-range

          bool oldOn = (oldByte & (1 << bit)) != 0;
          bool newOn = (newByte & (1 << bit)) != 0;

          if (oldOn != newOn) {
            MapEntry<bool, int> mapping = bitToKeyMap[linearIndex];
            bool isWhite = mapping.key;
            int keyIndex = mapping.value;

            if (isWhite) {
              whiteKeyPressed[keyIndex] = newOn;
            } else {
              blackKeyPressed[keyIndex] = newOn;
            }
          }
        }
      }

      // Save message for next comparison
      _lastMessage = List<int>.from(data);
    });
  }

  List<Widget> buildWhiteKeys(double whiteKeyWidth, double whiteKeyHeight) {
    return List.generate(whiteKeys.length, (index) {
      final isPressed = whiteKeyPressed[index] ?? false;
      return GestureDetector(
        onTapDown: (_) => setState(() => whiteKeyPressed[index] = true),
        onTapUp: (_) => setState(() => whiteKeyPressed[index] = false),
        onTapCancel: () => setState(() => whiteKeyPressed[index] = false),
        child: Container(
          width: whiteKeyWidth,
          height: whiteKeyHeight,
          decoration: BoxDecoration(
            color: isPressed ? Colors.yellow[200] : Colors.white,
            border: Border.all(color: Colors.black),
          ),
        ),
      );
    });
  }

  List<Widget> buildBlackKeys(double whiteKeyWidth, double blackKeyWidth, double blackKeyHeight) {
    List<Widget> keys = [];
    for (int i = 0; i < whiteKeys.length - 1; i++) {
      if (blackKeyPattern.containsKey(whiteKeys[i])) {
        final isPressed = blackKeyPressed[i] ?? false;
        double left = (i + 1) * whiteKeyWidth - blackKeyWidth / 2;
        keys.add(Positioned(
          left: left,
          top: 0,
          child: GestureDetector(
            onTapDown: (_) => setState(() => blackKeyPressed[i] = true),
            onTapUp: (_) => setState(() => blackKeyPressed[i] = false),
            onTapCancel: () => setState(() => blackKeyPressed[i] = false),
            child: Container(
              width: blackKeyWidth,
              height: blackKeyHeight,
              decoration: BoxDecoration(
                color: isPressed ? Colors.yellow[200] : Colors.black,
                border: Border.all(color: Colors.black, width: 1),
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(4),
                  bottomRight: Radius.circular(4),
                ),
              ),
            ),
          ),
        ));
      }
    }
    return keys;
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    const minWindowHeight = 350.0;
    const maxWindowHeight = 700.0;
    const minWhiteKeyHeight = 110.0;
    const maxWhiteKeyHeight = 180.0;

    double tLinear = ((screenHeight - minWindowHeight) / (maxWindowHeight - minWindowHeight)).clamp(0.0, 1.0);
    double t = 0.5 * tLinear * tLinear;

    final whiteKeyHeight = minWhiteKeyHeight + (maxWhiteKeyHeight - minWhiteKeyHeight) * t;
    final blackKeyHeight = whiteKeyHeight * blackKeyHeightRatio;
    final pianoWidth = screenWidth * 0.9;
    final whiteKeyWidth = pianoWidth / 52;
    final blackKeyWidth = whiteKeyWidth * blackKeyWidthRatio;

    const bottomExtensionWidth = 30.0;
    const topExtensionHeight = 100.0;

    return InteractiveViewer(
      child: SizedBox(
        width: pianoWidth + 2 * bottomExtensionWidth,
        height: whiteKeyHeight + topExtensionHeight,
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            // Wooden panel background
            Positioned(
              left: 0,
              top: 0,
              child: Container(
                width: pianoWidth + 2 * bottomExtensionWidth,
                height: whiteKeyHeight + topExtensionHeight,
                decoration: BoxDecoration(
                  image: const DecorationImage(
                    image: AssetImage('assets/gradient.png'),
                    fit: BoxFit.cover,
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
            // Piano keys
            Positioned(
              left: bottomExtensionWidth,
              top: topExtensionHeight,
              child: SizedBox(
                width: pianoWidth,
                height: whiteKeyHeight,
                child: Stack(
                  children: [
                    Row(children: buildWhiteKeys(whiteKeyWidth, whiteKeyHeight)),
                    ...buildBlackKeys(whiteKeyWidth, blackKeyWidth, blackKeyHeight),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
