import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../controllers/piano_udp_controller.dart';

class Piano extends StatefulWidget {
  /// Callback to notify parent about updated suggestion headers
  final void Function(Map<String, Uint8List>)? onSuggestionUpdate;

  const Piano({super.key, this.onSuggestionUpdate});

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};

  late PianoUdpController _udpController;

  // Ratios for black keys relative to white keys
  static const double blackKeyHeightRatio = 0.65;
  static const double blackKeyWidthRatio = 0.6;

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
    _udpController = PianoUdpController(
      onKeyUpdate: (isWhite, keyIndex, pressed) {
        setState(() {
          if (isWhite) {
            whiteKeyPressed[keyIndex] = pressed;
          } else {
            blackKeyPressed[keyIndex] = pressed;
          }
        });
      },
      onSuggestionUpdate: (suggestions) {
        // Notify the parent widget (Page1) about updated suggestions
        if (widget.onSuggestionUpdate != null) {
          widget.onSuggestionUpdate!(suggestions);
        }
      },
    );
    _udpController.start();
  }

  @override
  void dispose() {
    _udpController.dispose();
    super.dispose();
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
