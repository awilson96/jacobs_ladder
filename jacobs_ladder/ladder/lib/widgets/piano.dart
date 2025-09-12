import 'package:flutter/material.dart';
import 'dart:typed_data';

import '../controllers/piano_udp_controller.dart';

class Piano extends StatefulWidget {
  /// Callback to notify parent about updated suggestion headers
  final void Function(Map<String, Uint8List>)? onSuggestionUpdate;

  /// Filtered suggestion masks from Page1
  final Map<String, Uint8List> suggestionMasks;

  const Piano({
    super.key,
    this.onSuggestionUpdate,
    required this.suggestionMasks,
  });

  @override
  _PianoState createState() => _PianoState();
}

class _PianoState extends State<Piano> {
  final Map<int, bool> whiteKeyPressed = {};
  final Map<int, bool> blackKeyPressed = {};
  final Map<int, Color> keyColors = {}; // For suggestion/live colors

  late PianoUdpController _udpController;

  static const double blackKeyHeightRatio = 0.65;
  static const double blackKeyWidthRatio = 0.6;

  final List<String> whiteKeys = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B',
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
        if (widget.onSuggestionUpdate != null) {
          widget.onSuggestionUpdate!(suggestions);
        }
      },
      onKeyColorUpdate: (colors) {
        setState(() {
          keyColors.clear();
          keyColors.addAll(colors);
        });
      },
    );

    _udpController.start();

    // Pass initial suggestion masks to controller
    _udpController.setSuggestionMasks(widget.suggestionMasks);
  }

  @override
  void didUpdateWidget(covariant Piano oldWidget) {
    super.didUpdateWidget(oldWidget);

    // Update suggestion masks whenever they change
    if (oldWidget.suggestionMasks != widget.suggestionMasks) {
      _udpController.setSuggestionMasks(widget.suggestionMasks);
    }
  }

  @override
  void dispose() {
    _udpController.dispose();
    super.dispose();
  }

  Color _getKeyColor(int index, bool isWhite) {
    // Encode key to match controller
    int key = isWhite ? index : index + 100;

    if (keyColors.containsKey(key)) return keyColors[key]!;

    if (isWhite && (whiteKeyPressed[index] ?? false)) return Colors.red;
    if (!isWhite && (blackKeyPressed[index] ?? false)) return Colors.red;

    return isWhite ? Colors.white : Colors.black;
  }

  List<Widget> buildWhiteKeys(double whiteKeyWidth, double whiteKeyHeight) {
    return List.generate(whiteKeys.length, (index) {
      final color = _getKeyColor(index, true);
      return GestureDetector(
        onTapDown: (_) => setState(() => whiteKeyPressed[index] = true),
        onTapUp: (_) => setState(() => whiteKeyPressed[index] = false),
        onTapCancel: () => setState(() => whiteKeyPressed[index] = false),
        child: Container(
          width: whiteKeyWidth,
          height: whiteKeyHeight,
          decoration: BoxDecoration(
            color: color,
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
        final color = _getKeyColor(i, false);
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
                color: color,
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
