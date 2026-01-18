class MessageHeap {
  final int midiNote;
  final int instanceIndex;
  final int status;
  final int velocity;
  final int pitchBend; // 0–16383, 8192 = no bend

  MessageHeap({
    required this.midiNote,
    required this.instanceIndex,
    required this.status,
    required this.velocity,
    required this.pitchBend,
  });
}
