const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require("./source.js");
  
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
              swaps {
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

    await csv.toDisk(`/datasets/${keys}.csv`)

       
    } catch(error) {
      console.log(error);
    }
  };
  MAIN();
})});
