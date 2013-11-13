import 'dart:html';
import 'dart:math';
import 'dart:async';
import 'dart:collection';
import 'dart:convert';
import 'dart:typed_data';

var rng = new Random();
Queue dataQueue = new Queue();
int queueSize = 100;
WebSocket ws;
int count = 0;
var output = querySelector('#output');
var myimg = querySelector("#myimg");
CanvasElement canvas = querySelector("#canvas");
CanvasElement canvasM = querySelector("#canvasM");
CanvasElement canvasQ = querySelector("#canvasQ");
CanvasElement canvas4 = querySelector("#canvas4");
CanvasRenderingContext2D contextQ = canvasQ.getContext('2d');
CanvasRenderingContext2D context4 = canvas4.getContext('2d');
List lineUp = new Iterable.generate(queueSize, (i) => 5000).toList(growable: false);
int cmdId = 0;

bool showRgbJsonImg = true;
bool showRgbJsonDiff = true;
bool showJpgBinSrc = true;
bool showRgbBinImg = true;

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

drawRecArrayByIntList(CanvasElement ce, List rgbs){
  CanvasRenderingContext2D context = ce.getContext('2d');
  int w = ce.width;
  int h = ce.height;
  context.beginPath();
  context.clearRect(0, 0, w, h);
  context.fillStyle = '#ffffff';
  context.strokeStyle = '#000000';
  context.fillRect(0,0,w,h);
  int scale = 2;
  int size = 100;
  for (var i = 0; i < rgbs.length; i++) {
      int r = rgbs[i]>> 16 & 0xFF;
      int g = rgbs[i]>> 8 & 0xFF;
      int b = rgbs[i]&0xFF;
      String rgbStyle = "rgb($r,$g,$b)";
      //print(rgbStyle);
      context.fillStyle = rgbStyle;
      int x = (i%size)*scale;
      int y = (i/size).floor()*scale;
      //print("$x,$y");
      context.fillRect(x,y,scale,scale);
  } 
    context.stroke();
    context.closePath();
}

drawRecRgbUint8List(int w, int h, CanvasRenderingContext2D context, Uint8List rgbs){
  context.beginPath();
  context.clearRect(0, 0, w, h);
  context.fillStyle = '#ffffff';
  context.strokeStyle = '#000000';
  context.fillRect(0,0,w,h);
  int size = rgbs.length~/3;
  for (var i = 0; i < size; i++) {
      var r = rgbs[i*3];
      var g = rgbs[i*3+1];
      var b = rgbs[i*3+2];
      String rgbStyle = "rgb($r,$g,$b)";
      //print(rgbStyle);
      context.fillStyle = rgbStyle;
      int x = (i%w);
      int y = (i/w).floor();
      //print("$x,$y");
      context.fillRect(x,y,1,1);
  } 
    context.stroke();
    context.closePath();
}

drawDiffArray(int max){
  int w = canvasQ.width;
  int h = canvasQ.height;
  contextQ.beginPath();
  contextQ.clearRect(0, 0, w, h);
  contextQ.fillStyle = '#ffffff';
  contextQ.strokeStyle = '#000000';
  contextQ.fillRect(0,0,w,h);
  contextQ.fillStyle = '#ff0000';
  List r = dataQueue.toList(growable: false);
  for (var i = 0; i < r.length; i++) {
      int v = ((r[i]/max)*100*-1).floor() -1;
      //print(v);
      contextQ.fillRect(i*4,95,4,v);
  } 
    contextQ.stroke();
    contextQ.closePath();
}

testDrawCanvasRgb(){
  // R=FF0000=16711680
  // G=00FF00=65280
  // B=0000FF=255
  var rgbs = [16711680,65280,255,128,0,255];
  drawRecArrayByIntList(canvas,rgbs);
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
  
  loadBlobRgbArrayBuf(b){
    FileReader fileReader = new FileReader();
    print("Read Blob/ArrayBuffer size = ${b.size}");
    fileReader.onLoadEnd.listen((evt) {
      ByteBuffer k = evt.target.result;
      //print(k);
      Uint8List buffer = new Uint8List.view(k, 0, k.lengthInBytes);
      //print(buffer.length);
      drawRecRgbUint8List(100, 100, context4, buffer);
    }); 
    fileReader.readAsArrayBuffer(b);
  }
  
  loadBlobJpegReadUrl(b){
    FileReader fileReader = new FileReader();
    //print("read blob size = ${b.size}");
    fileReader.onLoadEnd.listen((evt) {
      myimg.src = evt.target.result;
    }); 
    fileReader.readAsDataUrl(b);
  }

  ws.onMessage.listen((MessageEvent e) {
      outputMsg('msg ${count} : is String ? = ${e.data is String}');
      if(e.data is String){
        List rlist = JSON.decode(e.data);
        outputMsg('msg ${count} : v=${rlist.length}');
        
        if(rlist.length==1){
          // cmd mode
          cmdId = rlist[0];
          print("Read CmdId = $cmdId");
          
        }else if(rlist.length==2){
          // python
          //  msg = []
          // msg.append(q)
          // msg.append(m)
          // m_tornado.WSHandler.wsSend(json.dumps(msg))
          List mlist = rlist[1];
         // outputMsg('msg ${count} : q=${rlist[0]}/m size=${mlist.length}');
          dataQueue.add(rlist[0]);
          if(dataQueue.length>lineUp.length){
            dataQueue.removeFirst();
          }
        drawDiffArray(10000);
        if(showRgbJsonDiff){          
          drawRecArrayByIntList(canvasM, mlist);
        }
      }else if(rlist.length==10000){
        // python
        //  f2 = picam.takeRGBPhotoWithDetails(width, height)
        //  m_tornado.WSHandler.wsSend(json.dumps(f2))
        if(showRgbJsonImg){
          drawRecArrayByIntList(canvas, rlist);          
        }
      }
     }else {
       // e.data not String what type?
       // testBlobArrayBuf(e.data);
       if(cmdId==5){
         if(showJpgBinSrc){
           loadBlobJpegReadUrl(e.data);             
         }
       }else if(cmdId==6){
         if(showRgbBinImg){
           loadBlobRgbArrayBuf(e.data);           
         }
       }
     }
  });
}


void main() {
  initWebSocket();
  dataQueue.addAll(new Iterable.generate(lineUp.length, (i) => 0));
  //testDraw();
  //testDrawCanvasRgb();
}

