class Lick {
  final int id;
  final String? name;
  final String type; // melody, chords, harmony, bassline
  final double length; // in seconds

  Lick({
    required this.id,
    this.name,
    required this.type,
    required this.length,
  });
}
