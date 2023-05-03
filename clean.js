const fs = require('fs');

// read tmp/data1.json and tmp/data2.json
let data1 = JSON.parse(fs.readFileSync('tmp/data1.json'));
let data2 = JSON.parse(fs.readFileSync('tmp/data2.json'));
// combine them
let data = data1.concat(data2);
// write to data.json
fs.writeFileSync('data.json', JSON.stringify(data));
// delete temp directory
fs.rmdirSync('tmp', { recursive: true });