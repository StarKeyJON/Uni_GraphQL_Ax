const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require('./source.js');
const { mainSchema } = require('./queries.js');

function Q() {
  Object.entries(sources).forEach(([key, value]) => {
    MAIN = async () => {
      try {
      const result = await axios.post(
          value, 
          {
              query: `
              ${ mainSchema }
              `
          } 
        )
        const csv = new ObjectsToCsv(result.data.data.swaps)
        
        await csv.toDisk(`./${key}.csv`)
        
        } catch(err) {
          console.error(err)
        }
      };
    MAIN();
  })}
Q();