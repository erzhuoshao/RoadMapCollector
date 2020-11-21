var page = require('webpage').create(),
    system = require('system'),
    fs = require('fs');

imname = system.args[1];
path = system.args[2];

page.onConsoleMessage = function(msg) {console.log(msg);fs.write(path, msg,'w');};
//page.open('http://localhost:8000/Desktop/csm4telecom/bound_debug.html?'+encodeURI(imname), function(status) {
page.open('C:/Users/邵尔卓/Desktop/SRT/csm4telecom/csm4telecom/bound.html', function(status) {
console.log(status)
    window.setTimeout(function () {
        console.log(encodeURI(imname));
        phantom.exit();
    }, 500);
});