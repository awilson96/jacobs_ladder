import 'package:flutter/material.dart';

class Piano extends StatefulWidget {
  const Piano({super.key});

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};

  // Ratios for black keys relative to white keys
  static const double blackKeyHeightRatio = 0.65;
  static const double blackKeyWidthRatio = 0.6;

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    // Scaling bounds
    const minWindowHeight = 350.0; // smallest vertical window
    const maxWindowHeight = 700.0; // cap growth
    const minWhiteKeyHeight = 110.0;
    const maxWhiteKeyHeight = 180.0;

    // Linear factor [0,1]
    double tLinear = ((screenHeight - minWindowHeight) /
            (maxWindowHeight - minWindowHeight))
        .clamp(0.0, 1.0);

    // Parabolic factor
    double t = 0.5 * tLinear * tLinear; // quadratic growth

    // Scale key heights
    final whiteKeyHeight =
        minWhiteKeyHeight + (maxWhiteKeyHeight - minWhiteKeyHeight) * t;
    final blackKeyHeight = whiteKeyHeight * blackKeyHeightRatio;

    // Piano width (fixed proportion of screen)
    final pianoWidth = screenWidth * 0.9;
    final double whiteKeyWidth = pianoWidth / 52;
    final double blackKeyWidth = whiteKeyWidth * blackKeyWidthRatio;

    final whiteKeys = [
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

    final blackKeyPattern = {'C': true, 'D': true, 'F': true, 'G': true, 'A': true};

    List<Widget> buildWhiteKeys() {
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

    List<Widget> buildBlackKeys() {
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

    // Panel dimensions
    const double bottomExtensionWidth = 30.0;
    const double topExtensionHeight = 100.0;

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
                    Row(children: buildWhiteKeys()),
                    ...buildBlackKeys(),
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
