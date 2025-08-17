import 'package:flutter/material.dart';

class Piano extends StatelessWidget {
  const Piano({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final whiteKeyCount = 52; // total white keys on an 88-key piano
    final whiteKeyWidth = screenWidth / whiteKeyCount;
    final whiteKeyHeight = 200.0;
    final blackKeyWidth = whiteKeyWidth * 0.6;
    final blackKeyHeight = whiteKeyHeight * 0.6;

    // White keys in order starting from A0
    final whiteKeys = [
      'A', 'B', // first partial octave
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C', 'D', 'E', 'F', 'G', 'A', 'B',
      'C' // final C8
    ];

    // Build white keys
    List<Widget> buildWhiteKeys() {
      return List.generate(whiteKeys.length, (index) {
        return GestureDetector(
          onTap: () {
            print('White key ${whiteKeys[index]} pressed');
          },
          child: Container(
            width: whiteKeyWidth,
            height: whiteKeyHeight,
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.black),
            ),
          ),
        );
      });
    }

    // Black keys appear after these white notes in an octave
    final blackKeyPattern = {'C': true, 'D': true, 'F': true, 'G': true, 'A': true};

    // Build black keys
    List<Widget> buildBlackKeys() {
      List<Widget> keys = [];
      for (int i = 0; i < whiteKeys.length - 1; i++) { // <-- skip last white key
        if (blackKeyPattern.containsKey(whiteKeys[i])) {
          double left = (i + 1) * whiteKeyWidth - blackKeyWidth / 2;
          keys.add(Positioned(
            left: left,
            top: 0,
            child: GestureDetector(
              onTap: () {
                print('Black key above ${whiteKeys[i]} pressed');
              },
              child: Container(
                width: blackKeyWidth,
                height: blackKeyHeight,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(4),
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
          Row(
            mainAxisSize: MainAxisSize.max,
            children: buildWhiteKeys(),
          ),
          ...buildBlackKeys(),
        ],
      ),
    );
  }
}
