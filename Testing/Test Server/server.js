//IMPORt PACKAGES
var express = require('express');
var app = express();
var fs = require('fs');
var bodyParser = require('body-parser')
var PythonShell = require('python-shell');
var errorhandler = require('errorhandler');
var KalmanFilter = require('kalmanjs').default;
var iter = 0;
var kal1 = new KalmanFilter({R: 0.008, Q: 3});
var kal2 = new KalmanFilter({R: 0.008, Q: 3});
var kal3 = new KalmanFilter({R: 0.008, Q: 3});
var kal4 = new KalmanFilter({R: 0.008, Q: 3});
var beak1 = [];
var beak2 = [];
var beak3 = [];
var beak4 = [];
function logResults( name, ein, zwei, drei, vier){
    console.log (name, " ", ein, " ", zwei, " ", drei, " ", vier);
    // console.log (ein);
    // console.log (zwei);
    // console.log (drei);
    // console.log (vier);
};
function manageBeak(beak, R){
    beak.push (R);
    if (beak.length > 20)
    {
        beak.shift();
    }
};
function kalFil(beak, kal){
    var fRSSI = beak.map(function(v) { return kal.filter(v);});
    return fRSSI[fRSSI.length-1];
};
function ablFil(beak){
    var tmp = beak.slice();
    var toavg = tmp.sort(function(a,b){ 
        return a - b
    })
    if (toavg.length < 3){
        ;
    }
    else if (toavg.length < 15){
        //console.log(toavg.length);
        toavg = toavg.slice(1,-1);
        //console.log(toavg.length);
    }
    else{
        //console.log(toavg.length);
        toavg = toavg.slice(2,-2);
        //console.log(toavg.length);
    }
    var sum = toavg.reduce(function(a, b) { return a + b; });
    return sum / toavg.length;
}
app.use(express.static(__dirname));
//Middleware for POST
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.post('/update', function(req,res) {
//store values from POST body
    console.log("post");
    iter = iter + 1;
    if (iter > 100){
        res.end();
        process.exit();
    }
    var R1 = parseInt(req.body['rssi1']);
    var R2 = parseInt(req.body['rssi2']);
    var R3 = parseInt(req.body['rssi3']);
    var R4 = parseInt(req.body['rssi4']);
    logResults("Unfiltered",R1, R2, R3, R4);
    manageBeak(beak1, R1);
    manageBeak(beak2, R2);
    manageBeak(beak3, R3);
    manageBeak(beak4, R4);
    logResults("Kalman", kalFil(beak1, kal1), kalFil(beak2, kal2), kalFil(beak3, kal3), kalFil(beak4, kal4));
    logResults("Android", ablFil(beak1), ablFil(beak2), ablFil(beak3), ablFil(beak4));
    res.end();
});
app.listen(8080, '192.168.1.69');