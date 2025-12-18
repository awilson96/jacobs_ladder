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

  // Private constructor
  UdpService._internal();

  /// Start receiving on the fixed port
  Future<void> start() async {
    if (_receiveSocket != null) return;

    // Bind receive socket
    _receiveSocket = await RawDatagramSocket.bind(_receiveHost, _receivePort);
    _receiveSocket!.listen(_onReceiveEvent);

    // Bind send socket on ephemeral port
    _sendSocket = await RawDatagramSocket.bind(InternetAddress.loopbackIPv4, 0);

    print('UDP receive socket bound to ${_receiveSocket!.address.address}:${_receiveSocket!.port}');
    print('UDP send socket bound to ${_sendSocket!.address.address}:${_sendSocket!.port}');
  }

  void _onReceiveEvent(RawSocketEvent event) {
    if (event == RawSocketEvent.read) {
      final datagram = _receiveSocket!.receive();
      if (datagram != null) {
        _incomingController.add(datagram.data);
      }
    }
  }

  /// Send data to the fixed send address/port
  void send(Uint8List data) {
    _sendSocket?.send(data, _sendHost, _sendPort);
  }

  /// Stop the service
  Future<void> stop() async {
    await _incomingController.close();
    _receiveSocket?.close();
    _receiveSocket = null;
    _sendSocket?.close();
    _sendSocket = null;
  }
}
