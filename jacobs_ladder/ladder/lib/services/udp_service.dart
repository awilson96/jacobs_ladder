import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

class UdpService {
  // Singleton instance
  static final UdpService _instance = UdpService._internal();
  factory UdpService() => _instance;

  // Fixed send target
  final InternetAddress _sendHost = InternetAddress.loopbackIPv4;
  final int _sendPort = 50000;

  // Fixed receive bind
  final InternetAddress _receiveHost = InternetAddress.loopbackIPv4;
  final int _receivePort = 50005;

  RawDatagramSocket? _receiveSocket;
  RawDatagramSocket? _sendSocket;
  final _incomingController = StreamController<Uint8List>.broadcast();

  Stream<Uint8List> get messages => _incomingController.stream;

  bool _sendReady = false;
  final List<Uint8List> _sendQueue = [];

  // Private constructor
  UdpService._internal();

  /// Start receiving on the fixed port
  Future<void> start() async {
    if (_receiveSocket != null) {
      return;
    }

    try {
      _receiveSocket = await RawDatagramSocket.bind(_receiveHost, _receivePort);
      _receiveSocket!.listen(_onReceiveEvent, onError: (e) {
        print('UDPService: receive socket error: $e');
      }, onDone: () {});
    } catch (e) {
      print('UDPService: failed to bind receive socket: $e');
    }

    try {
      // Bind send socket to any interface
      _sendSocket = await RawDatagramSocket.bind(InternetAddress.loopbackIPv4, 0);
      _sendSocket!.listen(_onSendEvent, onError: (e) {
        print('UDPService: send socket error: $e');
      }, onDone: () {});
    } catch (e) {
      print('UDPService: failed to bind send socket: $e');
    }
  }

  void _onReceiveEvent(RawSocketEvent event) {
    if (event == RawSocketEvent.read) {
      final datagram = _receiveSocket!.receive();
      if (datagram != null) {
        _incomingController.add(datagram.data);
      }
    }
  }

  void _onSendEvent(RawSocketEvent event) {
    if (event == RawSocketEvent.write) {
      _sendReady = true;
      // Flush queued messages
      while (_sendQueue.isNotEmpty) {
        final data = _sendQueue.removeAt(0);
        _sendNow(data);
      }
    }
  }

  void _sendNow(Uint8List data) {
    if (_sendSocket == null) return;

    final sent = _sendSocket!.send(data, _sendHost, _sendPort);
    if (sent == 0) {
      _sendQueue.add(data);
    }
  }

  /// Send data to the fixed send address/port
  void send(Uint8List data) {
    if (_sendSocket == null) {
      return;
    }

    if (_sendReady) {
      _sendNow(data);
    } else {
      _sendQueue.add(data);
    }
  }

  /// Stop the service
  Future<void> stop() async {
    await _incomingController.close();
    _receiveSocket?.close();
    _receiveSocket = null;
    _sendSocket?.close();
    _sendSocket = null;
    _sendQueue.clear();
    _sendReady = false;
  }
}
