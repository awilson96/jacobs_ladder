import 'package:flutter/material.dart';
import '../widgets/piano.dart';

class Page1 extends StatelessWidget {
  const Page1({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          const Align(
            alignment: Alignment.topCenter,
            child: Padding(
              padding: EdgeInsets.only(top: 24),
              child: Text('Page 1', style: TextStyle(fontSize: 20)),
            ),
          ),

          // Piano anchored to the bottom-center
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Center(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: const Piano(),
              ),
            )
          ),
        ],
      ),
    );
  }
}