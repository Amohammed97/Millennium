
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

https.createServer(options, function (req, res) {
  
  if (req.method === "GET") {

    res.writeHead(200, { "Content-Type": "text/html" });
    //res.json({"foo": "bar"}); 
    res.end(JSON.stringify({ a: 1 }));

  } 
  
  else if (req.method === "POST") {
    var body = "";
    req.on("data", function (chunk) {
        body += chunk;
    });

    req.on("end", function(){
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(body);
        console.log(body)
        
    });

  }

}).listen(8000 , "192.168.1.89");

