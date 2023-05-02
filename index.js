const async = require('async');
const fs = require('fs');
const util = require('minecraft-server-util');
// ips.txt contains a list of IP addresses, one per line
let ips = fs.readFileSync('ips.txt').toString().split('\n');
const startTime = new Date();
let results = [];

// async every 10 seconds, save results to data.json
const saveData = async () => {
    fs.writeFileSync('data.json', JSON.stringify(results));
}
setInterval(saveData, 5000);
const progress = () => {
    // calculate percentage complete
    let percent = (found + dead) / ips.length * 100;
    percent = percent.toFixed(2);
    // calculate time passed
    let timePassed = new Date() - startTime;
    // format time passed
    process.stdout.write("%" + percent + " found " + found + " dead " + dead + " remaining " + remaining + "\r");
}
setInterval(progress, 5000); // slow but github actions cries if it's too fast
let found = 0;
let dead = 0;
let remaining = ips.length;
const getServerStatus = async (ip) => {
    remaining--;
    ip = ip.trim();
    return util.status(ip)
    .then((response) => {
        results.push(response);
        // console.log("len " + results.length)
        // console.log(ip + ": " + response)
        found++;
        // progress();
        return true;
    })
    .catch((error) => {
        // console.log(ip + ": " + error)
        dead++;
        // progress();
        return false;
        
    });
}

// let q = async.queue(getServerStatus, 1000);

// ips.forEach((ip) => {
//     // console.log("pushed " + ips.indexOf(ip))
//     q.push(ip);
// });
// ips = null;
// q.drain = () => {
//     fs.writeFileSync('data.json', JSON.stringify(results));
//     console.log("done");
// }
async.eachLimit(ips, 500, getServerStatus)
.then((res) => {
    fs.writeFileSync('data.json', JSON.stringify(results));
    progress();
    console.log();
    console.log("done");
    process.exit(0);
})
.catch((err) => {
    console.log(err)
    process.exit(1);
})