const async = require('async');
const fs = require('fs');
const util = require('minecraft-server-util');
const action = process.env.GITHUB_ACTIONS;
var ips = fs.readFileSync('ips.txt').toString().split('\n');
let outpath = 'data.json';
if (process.argv.length > 0) {
    if (process.argv[2] == '1') {
        // remove the second half of the ips
        ips = ips.slice(0, ips.length / 2);
        outpath = 'tmp/data1.json';
    }
    if (process.argv[2] == '2') {
        // remove the first half of the ips
        ips = ips.slice(ips.length / 2, ips.length);
        outpath = 'tmp/data2.json';
    }
    if (!fs.existsSync('tmp')) {
        fs.mkdirSync('tmp');
    }
}
console.log(ips.length);
console.log(process.argv[2]);
console.log()
let results = [];
fs.writeFileSync('data.json', '[]')
const saveData = async () => {
    fs.writeFileSync(outpath, JSON.stringify(JSON.parse(fs.readFileSync('data.json')).concat(results)));
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
            response.ip = ip;
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
    });
