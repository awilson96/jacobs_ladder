import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';

class Page2 extends StatefulWidget {
  const Page2({super.key});

  @override
  State<Page2> createState() => _Page2State();
}

class _Page2State extends State<Page2> {
  final List<String> genres = const [
    "Rock",
    "Pop",
    "Jazz",
    "Hip-Hop",
    "Classical",
    "Electronic",
    "Country",
    "Reggae",
    "Blues",
    "Metal",
  ];

  final ScrollController _scrollController = ScrollController();
  bool _hovering = false;

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final tabWidth = screenWidth / 7; // 1/7th of screen width

    return DefaultTabController(
      length: genres.length,
      child: Column(
        children: [
          SizedBox(
            height: 60, // enough room for tabs + scrollbar
            child: Listener(
              onPointerSignal: (pointerSignal) {
                if (pointerSignal is PointerScrollEvent) {
                  final newOffset = (_scrollController.offset +
                          pointerSignal.scrollDelta.dy)
                      .clamp(
                        0.0,
                        _scrollController.position.maxScrollExtent,
                      );
                  _scrollController.jumpTo(newOffset);
                }
              },
              child: MouseRegion(
                onEnter: (_) => setState(() => _hovering = true),
                onExit: (_) => setState(() => _hovering = false),
                child: Scrollbar(
                  controller: _scrollController,
                  thumbVisibility: _hovering, // only show on hover
                  thickness: 4,
                  radius: const Radius.circular(8),
                  child: SingleChildScrollView(
                    controller: _scrollController,
                    scrollDirection: Axis.horizontal,
                    physics: const BouncingScrollPhysics(),
                    child: TabBar(
                      isScrollable: true,
                      indicatorColor: Theme.of(context).colorScheme.primary,
                      tabs: genres
                          .map(
                            (genre) => SizedBox(
                              width: tabWidth,
                              child: Tab(text: genre),
                            ),
                          )
                          .toList(),
                    ),
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: TabBarView(
              children: genres
                  .map(
                    (genre) => Center(
                      child: Text(
                        genre,
                        style: const TextStyle(fontSize: 32),
                      ),
                    ),
                  )
                  .toList(),
            ),
          ),
        ],
      ),
    );
  }
}
