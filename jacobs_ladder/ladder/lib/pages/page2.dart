import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';

import '../models/licks.dart';
import '../widgets/play_button.dart';

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

  // temporary dummy data for now
  final Map<String, List<Lick>> genreLicks = {
    "Rock": [
      Lick(id: 1, name: "Power Riff", type: "Melody", length: 12.3),
      Lick(id: 2, name: "Groove Bass", type: "Bassline", length: 8.5),
    ],
    "Jazz": [
      Lick(id: 1, name: "Swing Line", type: "Harmony", length: 15.0),
      Lick(id: 2, name: null, type: "Chords", length: 10.2),
    ],
    // you can fill in other genres as needed
  };

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
            height: 60,
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
              children: genres.map((genre) {
                final licks = genreLicks[genre] ?? [];
                return SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: DataTable(
                    columnSpacing: 20,
                    headingRowColor: WidgetStateProperty.all(const Color.fromARGB(255, 52, 64, 52)),
                    columns: const [
                      DataColumn(label: Text("ID")),
                      DataColumn(label: Text("Name")),
                      DataColumn(label: Text("Type")),
                      DataColumn(label: Text("Length (s)")),
                      DataColumn(label: Text("Play")),
                    ],
                    rows: licks.map((lick) {
                      return DataRow(cells: [
                        DataCell(Text(lick.id.toString())),
                        DataCell(Text(lick.name ?? "—")),
                        DataCell(Text(lick.type)),
                        DataCell(Text(lick.length.toStringAsFixed(1))),
                        DataCell(PlayButton(lick: lick)),
                      ]);
                    }).toList(),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}