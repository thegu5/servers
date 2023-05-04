const fs = require('fs');

const data = JSON.parse(fs.readFileSync('data.json'));

console.log("# of servers: " + data.length);