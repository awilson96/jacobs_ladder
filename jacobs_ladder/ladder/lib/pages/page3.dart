import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class Page3 extends StatefulWidget {
  const Page3({super.key});

  @override
  State<Page3> createState() => _Page3State();
}

class _Page3State extends State<Page3> {
  bool _isRecording = false;
  int _tempoBpm = 120; // Default BPM
  RawDatagramSocket? _socket;
  final String _host = "127.0.0.1";
  final int _port = 50000;

  @override
  void initState() {
    super.initState();
    _initSocket();
  }

  Future<void> _initSocket() async {
    _socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 0);
  }

  void _sendRecordingMessage(bool start) {
    if (_socket == null) return;

    final int messageType = 1;
    final int recordingState = start ? 1 : 0;

    final builder = BytesBuilder();
    builder.add(_int32ToBytes(messageType));     // 4 bytes - message type
    builder.add(_int32ToBytes(recordingState));  // 4 bytes - start/stop
    builder.add(_int32ToBytes(_tempoBpm));       // 4 bytes - tempo BPM

    _socket!.send(builder.toBytes(), InternetAddress(_host), _port);
  }

  Uint8List _int32ToBytes(int value) {
    final bytes = ByteData(4);
    bytes.setUint32(0, value, Endian.big);
    return bytes.buffer.asUint8List();
  }

  void _toggleRecording() {
    setState(() {
      _isRecording = !_isRecording;
    });
    _sendRecordingMessage(_isRecording);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _isRecording ? "Recording..." : "Not recording",
              style: const TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              icon: Icon(_isRecording ? Icons.stop : Icons.mic),
              label: Text(_isRecording ? "Stop Recording" : "Start Recording"),
              style: ElevatedButton.styleFrom(
                backgroundColor: _isRecording ? Colors.red : Colors.green,
                padding:
                    const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              ),
              onPressed: _toggleRecording,
            ),
          ],
        ),
      ),

      // BPM control anchored at bottom center
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.symmetric(vertical: 20.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Tempo:",
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: 80,
              child: TextField(
                textAlign: TextAlign.center,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: "BPM",
                  isDense: true,
                  contentPadding:
                      EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                ),
                controller: TextEditingController(text: _tempoBpm.toString()),
                onSubmitted: (val) {
                  final parsed = int.tryParse(val);
                  if (parsed != null && parsed > 0) {
                    setState(() => _tempoBpm = parsed);
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _socket?.close();
    super.dispose();
  }
}
