const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require("./source.js");
const fs = require('fs');

// Get timestamp for each query

function TIMESTAMP() {
  Object.entries(sources).forEach(([key, value]) => {
    MAIN = async () => {
      try {
      const result = await axios.post(
          value, 
          {
              query: `
              {
                swaps (first: 100, orderBy: timestamp orderDirection: desc){
                  transaction{
                    id
                  }
                }
              }
              `
          } 
        )
        const csv = new ObjectsToCsv(result.data.data.swaps)
        
        await csv.toDisk(`./newtimesets/${key}timestamp.csv`)
        
        } catch(err) {
          //Error logging
          fs.stat('errorLog.txt', function (err, stat) {
            if (err == null) {
              fs.appendFile('errorLog.txt', err&&stat, function (err) {
                if (err) throw err;
              });
            } else if (err.code == 'ENOENT') {
              fs.writeFile('errorLog.txt', err&&stat, function (err) {
                if (err) throw err;
              });
            }
          });
        }
      };
    MAIN();
  })}
TIMESTAMP();
