const express = require('express');
const fs = require('fs');
const open = require('open')

//CREATE APP
const app = express();

app.use(express.static(__dirname));

//PORT TO LISTEN TO
const server = app.listen(3000, () => {
  console.log("Listening on localhost:3000");
  // open(`http://localhost:3000/index.html`)
});