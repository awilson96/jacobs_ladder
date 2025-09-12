class Lick {
  final int id;
  final String? name;
  final String type;
  final double length;
  final String? midiPath;

  Lick({
    required this.id,
    this.name,
    required this.type,
    required this.length,
    this.midiPath,
  });
}
