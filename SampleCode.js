//Sample code on how the API works in JavaScript
//API Key is removed for public viewing

var http = require("https");

var options = {
  "method": "GET",
  "hostname": "hashlookup.metascan-online.com",
  "path": "/v2/hash/E71A6D8760B37E45FA09D3E1E67E2CD3",
  "headers": {
    "apikey": ""
  }
};

var req = http.request(options, function (res) {
  var chunks = [];

  res.on("data", function (chunk) {
    chunks.push(chunk);
  });

  res.on("end", function () {
    var body = Buffer.concat(chunks);
    console.log(body.toString());
  });
});

req.end();
