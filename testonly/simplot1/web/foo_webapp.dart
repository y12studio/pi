import 'dart:html';
import 'package:simplot/simplot.dart';
import 'dart:math';
import 'dart:async';

var rng = new Random();

void main() {
  
  var plotArea = querySelector("#simPlotHere");
  
  new Timer.periodic(new Duration(seconds: 1), (_) {
    
    plotArea.children.clear();
    var lineUp = [40, 40, 40, 40, 40, 40, 40];
    var data = [rng.nextInt(24), rng.nextInt(20), 2, rng.nextInt(12), 6.3, rng.nextInt(30), rng.nextInt(10)];
    var dataPlot = plot(data,y2:lineUp,color1:'#3C3D36',color2:'#90AB76',container:'#simPlotHere');
    dataPlot..grid()..xlabel('XLabel', color: '#3C3D36')..ylabel('YLabel');
    
  });
  
  
}

void reverseText(MouseEvent event) {
  var text = querySelector("#sample_text_id").text;
  var buffer = new StringBuffer();
  for (int i = text.length - 1; i >= 0; i--) {
    buffer.write(text[i]);
  }
  querySelector("#sample_text_id").text = buffer.toString();
}
