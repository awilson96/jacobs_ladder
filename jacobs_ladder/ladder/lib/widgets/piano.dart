import 'package:flutter/material.dart';

class Piano extends StatefulWidget {
  const Piano({super.key});

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};

  static const double fixedPianoWidth = 1560.0;
  static const double whiteKeyHeight = 110.0;
  static const double blackKeyHeight = 70.0;
  static const double blackKeyWidthRatio = 0.6;

  @override
  Widget build(BuildContext context) {
    final double whiteKeyWidth = fixedPianoWidth / 52;
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

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: SizedBox(
        width: fixedPianoWidth + 2 * bottomExtensionWidth,
        height: whiteKeyHeight + topExtensionHeight, // ✅ no bottom extension
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            // Wooden panel background
            Positioned(
              left: 0,
              top: 0,
              child: Container(
                width: fixedPianoWidth + 2 * bottomExtensionWidth,
                height: whiteKeyHeight + topExtensionHeight, // ✅ stops at keys
                decoration: BoxDecoration(
                  image: const DecorationImage(
                    image: AssetImage('assets/gradient.png'),
                    fit: BoxFit.cover,
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),

            // Piano keys (shifted right to account for left extension)
            Positioned(
              left: bottomExtensionWidth,
              top: topExtensionHeight,
              child: SizedBox(
                width: fixedPianoWidth,
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
