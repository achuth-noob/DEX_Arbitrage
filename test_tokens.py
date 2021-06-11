tokens = {
    "USDC": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6
    },
    "DAI":{
          "address":"0x6B175474E89094C44Da98b954EedeAC495271d0F",
          "decimals":18
    },
    "UNI": {
        "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "decimals": 18
    },
    "WETH": {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "decimals": 18
    },
    "WBTC": {
        "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "decimals": 18
    },
    "YFI": {
        "address": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",
        "decimals": 18
    },
}

token_comb = [('USDC', 'DAI'),
 ('USDC', 'UNI'),
 ('USDC', 'WETH'),
 ('USDC', 'WBTC'),
 ('USDC', 'YFI'),
 ('DAI', 'UNI'),
 ('DAI', 'WETH'),
 ('DAI', 'WBTC'),
 ('DAI', 'YFI'),
 ('UNI', 'WETH'),
 ('UNI', 'WBTC'),
 ('UNI', 'YFI'),
 ('WETH', 'WBTC'),
 ('WETH', 'YFI'),
 ('WBTC', 'YFI')]