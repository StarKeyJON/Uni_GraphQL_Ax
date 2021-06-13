const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require('./time_slate.js');
const { mainSchema } = require('./queries.js');

function POST() {
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
        console.log('succesfully fecthed default schema')
        
        } catch(err) {
          console.error(err)
        }
      };
    MAIN();
  })}
POST();