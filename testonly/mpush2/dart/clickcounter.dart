/**
# Copyright 2013 Y12Studio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/
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
  
  int wcount = 0;
  var output;
  ImageElement myimg;
  CanvasElement canvasA;
  CanvasRenderingContext2D contextA;
  var cmdId = 1;
  ImageElement canvasImg;
  
  ClickCounter.created() : super.created() {    
    //myimg = shadowRoot.querySelector("#myimg");
    //myimg.src = 'https://www.google.com/images/srpr/logo11w.png';
    canvasImg = new ImageElement();
    output = shadowRoot.querySelector('#output');
    canvasA = shadowRoot.querySelector("#canvasA");
    contextA = canvasA.getContext('2d');
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

    String wsHost = window.location.hostname;
    String wsPort = window.location.port;
    
    // dart dev port
    if(wsPort=="3030"){
      wsHost = "192.168.2.42";
      wsPort = "8888";
    }

    
    String uri = 'ws://${wsHost}:${wsPort}/ws';
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
      
      retrySeconds = 2;
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
  
  drawStd(){
    // block https://code.google.com/p/dart/issues/detail?id=14565
    // fillRect black not work.
    contextA.fillStyle = '#000000';
    contextA.fillRect(5,220,100,12);
    
    //contextA.font="14px Arial";
    contextA.fillStyle = '#FFFF00';
    contextA.fillText("StdDev=${stdDev}",10,230);
  }
  
  loadBlobJpegReadUrl(b){
    FileReader fileReader = new FileReader();
    fileReader.onLoadEnd.listen((evt) {
      canvasImg.src = evt.target.result;
      contextA.drawImage(canvasImg, 0, 0);
      drawStd();
      wcount++;
    }); 
    fileReader.readAsDataUrl(b);
  }
  
  loadBlobJpegReadUrlOnlyImgSrc(b){
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
        drawStd();
        break;
      case 3:
        // pass
        break;
      default:
        break;
        
        }
    }
}


