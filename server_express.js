var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey  = fs.readFileSync('key.pem', 'utf8');
var certificate = fs.readFileSync('cert.pem', 'utf8');
const bodyParser = require("body-parser");
var credentials = {key: privateKey, cert: certificate};
var express = require('express');
var app = express();
var body = "";

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// your express configuration here
app.get('/', function (req, res) {

    res.json(body)  
    })

app.post('/',(req,res) => {
        //code to perform particular action.
        //To access POST variable use req.body()methods.
        console.log(req.body);
        body = req.body
        res.end();
        });


var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

httpServer.listen(8080,"192.168.1.89");
httpsServer.listen(8000,"192.168.1.89");