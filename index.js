const async = require('async');
const fs = require('fs');
const util = require('minecraft-server-util');
const action = process.env.GITHUB_ACTIONS;
let ips = fs.readFileSync('ips.txt').toString().split('\n');
let results = [];
fs.writeFileSync('data.json', '[]')
const saveData = async () => {
    fs.writeFileSync('data.json', JSON.stringify(JSON.parse(fs.readFileSync('data.json')).concat(results)));
    results = [];
    data = null;
}
// action ? setInterval(saveData, 60000) : setInterval(saveData, 5000);

const progress = () => {
    // calculate percentage complete
    let percent = (found + dead) / ips.length * 100;
    percent = percent.toFixed(2);
    process.stdout.write("%" + percent + " found " + found + " dead " + dead + " remaining " + remaining + "\r");
}
action ? setInterval(progress, 5000) : setInterval(progress, 500);
let found = 0;
let dead = 0;
let remaining = ips.length;

const getServerStatus = async (ip) => {
    remaining--;
    ip = ip.trim();
    return util.status(ip)
        .then((response) => {
            delete response.favicon;
            results.push(response);
            if (results.length > 1000) {
                saveData();
            }
            found++;
            return true;
        })
        .catch((error) => {
            dead++;
            return false;
        });
}

async.eachLimit(ips, 500, getServerStatus)
    .then((res) => {
        // const zlib = require('zlib');
        // const gzipData = zlib.gzipSync(JSON.stringify(results));
        // fs.writeFileSync('data.json.gz', gzipData);
        saveData();
        progress();
        console.log();
        console.log("done");
        process.exit(0);
    })
    .catch((err) => {
        console.log(err)
        process.exit(1);
    })
