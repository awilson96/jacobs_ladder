import 'package:flutter/material.dart';
import '../widgets/piano.dart';

class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    const minPianoWidth = 1560.0; // 52 white keys × 30 px minimum each

    return Column(
      children: [
        Expanded(
          child: Center(child: Text('Page 1')),
        ),
        // Piano with minimum width and horizontal scroll fallback
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: ConstrainedBox(
            constraints: BoxConstraints(minWidth: minPianoWidth),
            child: const Piano(),
          ),
        ),
      ],
    );
  }
}
