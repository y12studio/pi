import 'dart:html';
import 'package:simplot/simplot.dart';
import 'dart:math';
import 'dart:async';
import 'dart:collection';
// https://github.com/scribeGriff/simplot

var rng = new Random();
var dataQueue = new Queue();
int queueSize = 60;
WebSocket ws;
int count = 0;
var output = querySelector('#output');
var plotArea = querySelector("#simPlotHere");
List lineUp = new Iterable.generate(queueSize, (i) => 5000).toList(growable: false);

outputMsg(String msg) {
  if(count++%queueSize==0){
    output.text = '';
  }
  var text = msg;
  if (!output.text.isEmpty) {
    text = "${text}\n${output.text}";
  }
  output.text = text;
}

void initWebSocket([int retrySeconds = 2]) {
  var reconnectScheduled = false;
  
  String host = "192.168.2.42";
  String port = "8888";

  //String host = window.location.hostname;
  // String port = window.location.port;
  
  String uri = 'ws://${host}:${port}/ws';
  outputMsg("Connecting to websocket $uri");
  ws = new WebSocket(uri);

  void scheduleReconnect() {
    if (!reconnectScheduled) {
      new Timer(new Duration(milliseconds: 1000 * retrySeconds), () => initWebSocket(retrySeconds * 2));
    }
    reconnectScheduled = true;
  }

  ws.onOpen.listen((e) {
    outputMsg('Connected');
    ws.send('Hello from Dart!');
  });

  ws.onClose.listen((e) {
    outputMsg('Websocket closed, retrying in $retrySeconds seconds');
    scheduleReconnect();
  });

  ws.onError.listen((e) {
    outputMsg("Error connecting to ws");
    scheduleReconnect();
  });

  ws.onMessage.listen((MessageEvent e) {
    outputMsg('msg ${count} : ${e.data}');
    dataQueue.add(int.parse(e.data));
    if(dataQueue.length>lineUp.length){
      dataQueue.removeFirst();
    }
    drawQueue();
    
  });
}

void main() {
  initWebSocket();
  dataQueue.addAll(new Iterable.generate(lineUp.length, (i) => 0));
  //testDraw();
}

drawQueue(){
    plotArea.children.clear();
    //var lineUp = [40, 40, 40, 40, 40, 40, 40];
    List data = dataQueue.toList(growable: false);
    var dataPlot = plot(data,y2:lineUp,color1:'#3C3D36',color2:'#90AB76',container:'#simPlotHere',range:1, index:1);
    dataPlot..grid()..xlabel('XLabel', color: '#3C3D36')..ylabel('YLabel');
 
}

testDraw(){
 new Timer.periodic(new Duration(seconds: 1), (_) {
    plotArea.children.clear();
    var lineUp = [40, 40, 40, 40, 40, 40, 40];
    var data = [rng.nextInt(24), rng.nextInt(20), 2, rng.nextInt(12), 6.3, rng.nextInt(30), rng.nextInt(10)];
    var dataPlot = plot(data,y2:lineUp,color1:'#3C3D36',color2:'#90AB76',container:'#simPlotHere',range:1, index:1);
    dataPlot..grid()..xlabel('XLabel', color: '#3C3D36')..ylabel('YLabel');
  });
}
