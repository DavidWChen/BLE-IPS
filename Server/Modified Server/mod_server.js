var express = require('express');
var app = express();
var fs = require('fs');
var bodyParser = require('body-parser');

app.get('/data', function (req, res) {
   fs.readFile( __dirname + "/" + "txyz.json", 'utf8', function (err, data) {
       console.log( data );
       res.end( data );
   });
});

app.get('/:id', function (req, res) {
    fs.readFile( __dirname + "/" + "txyz.json", 'utf8', function (err, data) {
      var chip = JSON.parse( data );
      var chips = chip["chip" + req.params.id] 
      console.log( chips );
      res.end( JSON.stringify(chips));
   });
})

app.use(bodyParser.json());

app.use(bodyParser.urlencoded( {
    extended: true
}));

app.post('/update', function(req,res) { //client posts
    fs.readFile( __dirname + "/" + "txyz.json", 'utf8', function (err, data) {
        var newchip = req.body;
        data = JSON.parse( data );
        // Object.keys(newchip).forEach(function(k)
        var dataKey = Object.keys(newchip).toString();
        data[dataKey] = newchip[dataKey];
        // var hasData = data.hasOwnProperty((dataKey));
        var datastring = JSON.stringify(data);
        res.end(datastring);
        fs.writeFile(__dirname + "/" + "txyz.json", datastring, 'utf8',function (err) {
            if (err) throw err;
        });
    });
});

app.listen(8080, '192.168.1.77');