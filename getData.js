const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require("./source.js");
const fs = require('fs');
  
const keys = Object.keys(sources);
const values = Object.values(sources);

keys.forEach(function (keys) {
  values.forEach(function(values) {
    const MAIN = async () => {
    try {
    const result = await axios.post(
        values, 
        {
            query: `
            {
                swaps(orderBy: timestamp, orderDirection: desc){
                  timestamp
                  pair {
                    token0 {
                        name
                    }
                    token1 {
                        name
                    }
                  }
                  sender
                  amount0In
                  amount1In
                  amount0Out
                  amount1Out
                  to
                  amountUSD
                }
              }
            `
        } 
      )
        const csv = new ObjectsToCsv(result.data.data.swaps)
      
        await csv.toDisk(`./${keys}.csv`)

      } catch(error) {
        //Error logging
        fs.stat('errorLog.txt', function (err, stat) {
          if (err == null) {
            fs.appendFile('errorLog.txt', csv, function (err) {
              if (err) throw err;
            });
          } else if (err.code == 'ENOENT') {
            fs.writeFile('errorLog.csv', err, function (err) {
              if (err) throw err;
            });
          }
        });
      }
    };
    MAIN();
  })
});
