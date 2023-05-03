const fs = require('fs');

let data1 = JSON.parse(fs.readFileSync('tmp/data1.json'));
let data2 = JSON.parse(fs.readFileSync('tmp/data2.json'));

let data = data1.concat(data2);

fs.writeFileSync('data.json', JSON.stringify(data));

fs.rmSync('tmp', { recursive: true });