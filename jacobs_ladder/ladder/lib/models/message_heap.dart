class MessageHeap {
  final int midiNote;
  final int instanceIndex;
  final int status;
  final int velocity;
  final PitchInfo pitchInfo;

  MessageHeap({
    required this.midiNote,
    required this.instanceIndex,
    required this.status,
    required this.velocity,
    required this.pitchInfo,
  });
}

class PitchInfo {
  final int analogAbs;
  final int analogRel;
  final double cents;
  final int noteOrder;
  final String ratio;
  final String direction;

  PitchInfo({
    required this.analogAbs,
    required this.analogRel,
    required this.cents,
    required this.noteOrder,
    required this.ratio,
    required this.direction,
  });
}

