// npm install d3
// run as node 6 change startDate endDate
// node ./batchRun.js

const exec = require('child_process').exec;
var d3 = require("d3");

var formatHKJC = d3.timeFormat("%Y%m%d")
var formatMonth = d3.timeFormat("%B");
var startDate = new Date(2011, 01, 1);
var endDate = new Date(2011, 12, 31);

// d3.utcDay.offset(new Date(), 1)

var range = d3.utcDay.range(startDate, endDate);
//you could remove all dates in AUGUST!
var candiDates = range.map(d => {return formatHKJC(d);});


for (let d of candiDates) {
  console.time("loop start");
  let theCommand = `scrapy crawl racers -a racedate=${d}`
  console.log(theCommand);
  const child = exec(theCommand,
      (error, stdout, stderr) => {
          console.log(`stdout: ${stdout}`);
          console.log(`stderr: ${stderr}`);
          if (error !== null) {
              console.log(`exec error: ${error}`);
          }
  });

};
console.timeEnd("loop start");
