var express = require('express');
var serveStatic = require('serve-static');
var colors = require('colors');

var pubsub = require('./pubsub.js');
var util = require('./util.js');

var app = express();

app.use(serveStatic('public', {
    'index': ["index.html"]
}));

util.debug("[WEB   ]".green, "Serving static files on port 8080");
app.listen(8080);
