const axios = require('axios')
const ObjectsToCsv = require('objects-to-csv')

const main = async () => {
    try {
    const result = await axios.post(
        'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', 
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
    );
    
const csv = new ObjectsToCsv(result.data.data.swaps);

await csv.toDisk('./uni.csv');

//console.log(result.data.data.swaps);

} catch(error) {
    console.log(error);
}

}
main();
