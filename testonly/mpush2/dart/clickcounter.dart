import 'package:polymer/polymer.dart';
import 'dart:html';
import 'dart:async';
import 'dart:convert';

/**
 * A Polymer click counter element.
 */
@CustomTag('click-counter')
class ClickCounter extends PolymerElement {
  @published int stdDev = 0;
  @published int std1 = 0;
  @published int std2 = 0;
  @published int std3 = 0;
  @published int std4 = 0;
  @published int std5 = 0;
  @published int std6 = 0;
  @published int std7 = 0;
  @published int std8 = 0;
  @published int std9 = 0;
  
  int wcount = 0;
  var output;
  ImageElement myimg;
  var cmdId = 1;
  
  ClickCounter.created() : super.created() {    
    myimg = shadowRoot.querySelector("#myimg");
    output = shadowRoot.querySelector('#output');
    myimg.src = 'https://www.google.com/images/srpr/logo11w.png';
    initWebSocket();
  }
  
  outputMsg(String msg) {
    if(wcount%100==0){
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
    WebSocket ws = new WebSocket(uri);

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
      //outputMsg('msg ${count} : is String ? = ${e.data is String}');
      if(e.data is String){
        //outputMsg('msg ${count} : json = ${e.data}');
        List rlist = JSON.decode(e.data); 
        cmdId = rlist[0];
        if(rlist.length>=2){
           handleJsonResp(rlist);
        }
     } else {
       // e.data not String what type?
       // testBlobArrayBuf(e.data);
       if(cmdId==1){
           loadBlobJpegReadUrl(e.data);             
       }
     }
  });
}
  
  loadBlobJpegReadUrl(b){
    FileReader fileReader = new FileReader();
    fileReader.onLoadEnd.listen((evt) {
      myimg.src = evt.target.result;
      wcount++;
    }); 
    fileReader.readAsDataUrl(b);
  }
  
  handleJsonResp(List rlist) {
    switch (cmdId){
      case 2:
        // print std dev
        stdDev = rlist[1];
        outputMsg('msg ${wcount} : stddev = $stdDev');
        break;
      case 3:
        List r = rlist[1];
        std1 = r[0];
        std2 = r[1];
        std3 = r[2];
        std4 = r[3];
        std5 = r[4];
        std6 = r[5];
        std7 = r[6];
        std8 = r[7];
        std9 = r[8];
        //outputMsg('msg ${count} : stdarr = $r');
        break;
      default:
        break;
        
        }
    }
}


