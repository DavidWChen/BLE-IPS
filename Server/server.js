//IMPORT PACKAGES
var express = require('express');
var app = express();
var fs = require('fs');
var bodyParser = require('body-parser')
var PythonShell = require('python-shell');
var errorhandler = require('errorhandler');
var KalmanFilter = require('kalmanjs').default;
//Init
var ptime = 0;
var kal1 = new KalmanFilter({R: 0.008, Q: 3});
var kal2 = new KalmanFilter({R: 0.008, Q: 3});
var kal3 = new KalmanFilter({R: 0.008, Q: 3});
var kal4 = new KalmanFilter({R: 0.008, Q: 3});
var beak1 = [];
var beak2 = [];
var beak3 = [];
var beak4 = [];
//Constant (ms)
var period = 1000;
//Functions
function manageBeak(beak, R){
    //Add the newest RSSI to the list
    beak.push (R);
    if (beak.length > 20)
    {
        //Keep the list at size =20
        beak.shift();
    }
};
function kalFil(beak, kal){
    //apply a kalman filter to every item on the list and return the most recent value
    var fRSSI = beak.map(function(v) { return kal.filter(v);});
    return fRSSI[fRSSI.length-1];
};

app.use(express.static(__dirname));

//default
app.get('/',function(req,res) {
    res.send('IPS Home');
});

//displays data in txyz
app.get('/data', function (req, res) {
   fs.readFile( __dirname + "/" + "txyz.json", 'utf8', function (err, data) {
       res.end( data );
   })
});

//Middleware for POST
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.post('/update', function(req,res) {
    //check if enough time has passed
    if (Date.now() < (ptime + period)) {
        res.end();
        return;
    }
    ptime = Date.now();

    //store values from POST body
    var R1 = parseInt(req.body['rssi1']);
    var R2 = parseInt(req.body['rssi2']);
    var R3 = parseInt(req.body['rssi3']);
    var R4 = parseInt(req.body['rssi4']);
    manageBeak(beak1, R1);
    manageBeak(beak2, R2);
    manageBeak(beak3, R3);
    manageBeak(beak4, R4);
    var KR1 = kalFil(beak1, kal1);
    var KR2 = kalFil(beak2, kal2);
    var KR3 = kalFil(beak3, kal3);
    var KR4 = kalFil(beak4, kal4);
    //Python Shell options
    var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python2.7',
        pythonOptions: ['-u'],
        scriptPath: __dirname + "/",
        args: [KR1, KR2, KR3, KR4]
    };
    
    //Spawn Python shell to run RSSI-coordinate conversion
    PythonShell.run('server_rme.py', options, function (err, results) {
        if (err) throw err;
        //results array contains messages collected during execution (print)
        fs.readFile( __dirname + "/" + "txyz.json", 'utf8', function (err, data) {
            //parse python shell output, read and parse txyz.json
            results = JSON.stringify(JSON.parse(results));
            console.log(results);
            res.end(results);
            fs.writeFile(__dirname + "/" + "txyz.json", results, 'utf8',function (err) {
                if (err) throw err;
                console.log('Write Successful');
            });
        });
    });
});
app.listen(8080, '192.168.1.42');