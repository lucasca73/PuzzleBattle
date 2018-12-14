var http = require('http'),
  fs = require('fs');

fs.readFile('./game.html', function (err, html) {
  if (err) {
      throw err; 
  }
  http.createServer(function(request, response) {  
      response.writeHeader(200, {"Content-Type": "text/html"});  
      response.write(html);  
      response.end();  
  }).listen(3000, function () {
    console.log('Listening on http://localhost:' + (process.env.PORT || 3000))
  });
});
