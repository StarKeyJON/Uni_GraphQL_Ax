const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv');
const { sources } = require("./source.js");

//Create new variables from the key:values object in sources
const keys = Object.keys(sources);
const values = Object.values(sources);

//Create sleep function
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

const postData = keys.forEach(function (keys) {
  do {
  //iterate over each object in keys and initiate function
  keys.forEach(function (keys) {
  //for each key item, iterate over each object in values and initiate the main function
  values.forEach(function(values) {
   //send the fetch request and save the returned results to a new csv file
   const MAIN = async () => {
   try {
   const result = await axios.post(
       values, //api link variable 
        {
          //I will create this as a variable that the user chooses eventually
          //some graph schemas are structured differently as well
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
    //saving each returned object into a new csv file named with its own variable
     await csv.toDisk(`/datasets/${keys}.csv`)
     
     sleep(15000);
     
      } catch(error) {
        pass;
      }
    };
    MAIN();
  })
} while (true);
});
postData();
