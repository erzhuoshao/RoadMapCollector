var page = require('webpage').create(),
    system = require('system'),
    fs = require('fs'),
    wlen,hlen,path,i,j,data;

i = system.args[1];
j = system.args[2];
path = system.args[3];
wlen = system.args[4];
hlen = system.args[5];
leftup = system.args[6].split(',');
maplevel = system.args[7];
visibilitystate = system.args[8];

imname = './merge/'+i+'-'+j+'.jpeg';
leftmove = i*wlen,downmove = j*hlen;
data = leftup[0]+'&'+leftup[1]+'&'+'-'+leftmove+'&'+'-'+downmove+'&'+maplevel+'&'+visibilitystate;
//百度地图默认移动方向是左上，这里用负号改为右下，因此最开始需要指定所选区域的右上角经纬度坐标

page.onConsoleMessage = function(msg) {fs.write(path, i+'-'+j+':'+msg,'a+');};
page.viewportSize = { width: wlen, height: hlen };
page.clipRect = { top: 0, left: 0, width: wlen, height: hlen };

page.open('http://localhost:8000/Desktop/csm4telecom/ditu.html?'+data, function() {
  window.setTimeout(function () {
                console.log(imname);
                page.render(imname,{format: 'jpeg', quality: '100'});
                phantom.exit();
            }, 200);
});

