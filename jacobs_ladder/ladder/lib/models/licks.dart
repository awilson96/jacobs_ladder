class Lick {
  final String name;      // required unique identifier
  final String type;      // required
  final double length;    // derived from MIDI
  final String? midiPath; // optional

  Lick({
    required this.name,
    required this.type,
    required this.length,
    this.midiPath,
  });
}
