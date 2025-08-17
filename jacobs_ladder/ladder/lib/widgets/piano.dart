import 'package:flutter/material.dart';

class Piano extends StatefulWidget {
  const Piano({super.key});

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final usableWidth = screenWidth < 1560 ? 1560 : screenWidth;
    final whiteKeyWidth = usableWidth / 52;


    // Original heights (real-world proportions)
    final originalWhiteKeyHeight = 220.0;
    final originalBlackKeyHeight = originalWhiteKeyHeight * (3.5 / 5.5);

    // Scale down vertically by 50%
    final whiteKeyHeight = originalWhiteKeyHeight * 0.5; // 110 px
    final blackKeyHeight = originalBlackKeyHeight * 0.5; // ~70 px
    final blackKeyWidth = whiteKeyWidth * 0.6; // width ratio unchanged

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
                    topLeft: Radius.zero,
                    topRight: Radius.zero,
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

    return SizedBox(
      height: whiteKeyHeight,
      child: Stack(
        children: [
          Row(children: buildWhiteKeys()),
          ...buildBlackKeys(),
        ],
      ),
    );
  }
}
