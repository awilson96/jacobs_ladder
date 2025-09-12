import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';

import '../models/licks.dart';
import '../widgets/lick_table.dart';
import '../widgets/add_lick_dialog.dart';

class Page2 extends StatefulWidget {
  const Page2({super.key});

  @override
  State<Page2> createState() => _Page2State();
}

class _Page2State extends State<Page2> {
  final List<String> genres = const [
    "Rock", "Pop", "Jazz", "Hip-Hop", "Classical",
    "Electronic", "Country", "Reggae", "Blues", "Metal"
  ];

  final Map<String, List<Lick>> genreLicks = {
    "Rock": [
      Lick(name: "Power Riff", type: "Melody", length: 12.3),
      Lick(name: "Groove Bass", type: "Bassline", length: 8.5),
    ],
    "Jazz": [
      Lick(name: "Swing Line", type: "Harmony", length: 15.0),
      Lick(name: "Jazz Chords", type: "Chords", length: 10.2),
    ],
  };

  final ScrollController _scrollController = ScrollController();
  bool _hovering = false;

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final tabWidth = screenWidth / 7;

    return DefaultTabController(
      length: genres.length,
      child: Scaffold(
        body: Column(
          children: [
            SizedBox(
              height: 60,
              child: Listener(
                onPointerSignal: (pointerSignal) {
                  // Horizontal scroll using mouse wheel
                  if (pointerSignal is PointerScrollEvent) {
                    final newOffset = (_scrollController.offset + pointerSignal.scrollDelta.dy)
                        .clamp(0.0, _scrollController.position.maxScrollExtent);
                    _scrollController.jumpTo(newOffset);
                  }
                },
                child: MouseRegion(
                  onEnter: (_) => setState(() => _hovering = true),
                  onExit: (_) => setState(() => _hovering = false),
                  child: Scrollbar(
                    controller: _scrollController,
                    thumbVisibility: _hovering,
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
                            .map((genre) => SizedBox(width: tabWidth, child: Tab(text: genre)))
                            .toList(),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              child: TabBarView(
                children: genres.map((genre) {
                  return LickTable(
                    genre: genre,
                    licks: genreLicks[genre] ?? [],
                    onDelete: (lick) {
                      setState(() {
                        genreLicks[genre]?.remove(lick);
                      });
                    },
                  );
                }).toList(),
              ),
            ),
          ],
        ),
        floatingActionButton: Builder(
          builder: (context) {
            final tabIndex = DefaultTabController.of(context).index;
            return FloatingActionButton(
              onPressed: () => showAddLickDialog(
                context,
                genre: genres[tabIndex],
                onAdd: (newLick) {
                  setState(() {
                    genreLicks.putIfAbsent(genres[tabIndex], () => []);
                    genreLicks[genres[tabIndex]]!.add(newLick);
                  });
                },
              ),
              child: const Icon(Icons.add),
            );
          },
        ),
      ),
    );
  }
}
