const mainSchema = (
`
{
    swaps(first: 100, orderBy: timestamp, orderDirection: desc){
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
);

module.exports = { mainSchema };
