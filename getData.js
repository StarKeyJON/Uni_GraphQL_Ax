const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require("./source.js");
const fs = require('fs');
const { defaultSchema } = require("./queries.js");

function POST() {
  Object.entries(sources).forEach(([key, value]) => {
    MAIN = async () => {
      try {
      const result = await axios.post(
          value, 
          {
              query: `
              ${defaultSchema}
              `
          } 
        )
        const csv = new ObjectsToCsv(result.data.data.swaps)
        
        await csv.toDisk(`./${key}.csv`)
        
        } catch(err) {
          //Error logging
          fs.stat('errorLog.txt', function (err, stat) {
            if (err == null) {
              fs.appendFile('errorLog.txt', err&&stat, function (err) {
                if (err) throw err;
              });
            } else if (err.code == 'ENOENT') {
              fs.writeFile('errorLog.csv', err&&stat, function (err) {
                if (err) throw err;
              });
            }
          });
        }
      };
    MAIN();
  })}
POST();
