import 'dart:async'; 
import 'package:flutter/material.dart';

import '../models/licks.dart';

class PlayButton extends StatefulWidget {
  final Lick lick;
  const PlayButton({super.key, required this.lick});

  @override
  State<PlayButton> createState() => _PlayButtonState();
}

class _PlayButtonState extends State<PlayButton> {
  bool _isPlaying = false;
  double _remaining = 0;
  Timer? _timer;

  void _togglePlay() {
    if (_isPlaying) {
      _stop();
    } else {
      _start();
    }
  }

  void _start() {
    setState(() {
      _isPlaying = true;
      _remaining = widget.lick.length;
    });

    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_remaining <= 1) {
        _stop();
      } else {
        setState(() => _remaining--);
      }
    });

    // TODO: send UDP message to backend here
  }

  void _stop() {
    _timer?.cancel();
    setState(() {
      _isPlaying = false;
      _remaining = 0;
    });

    // TODO: send stop message if needed
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        IconButton(
          icon: Icon(_isPlaying ? Icons.pause : Icons.play_arrow),
          onPressed: _togglePlay,
        ),
        if (_isPlaying) Text("${_remaining.toInt()}s"),
      ],
    );
  }
}
