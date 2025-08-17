import 'package:flutter/material.dart';
import '../widgets/piano.dart';

class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: Center(child: Text('Page 1')),
        ),
        // Piano container
        Center(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: const Piano(),
          ),
        ),
      ],
    );
  }
}
