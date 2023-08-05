evm_network = {
    'ethereum': {
        "chainId": 1,
        "rpcUrl": "https://mainnet.infura.io/v3/INFURA_API_KEY"
    },
    'Optimistic': {
        "chainId": 10,
        "rpcUrl": "https://mainnet.optimism.io/",
    },
    'polygon': {
        "chainId": 137,
        "rpcUrl": "https://rpc-mainnet.matic.network"
    },
    'fantom': {
        "chainId": 250,
        "rpcUrl": "https://rpcapi.fantom.network"
    },
    'binance-smart-chain': {
        "chainId": 56,
        "rpcUrl": "https://bsc-dataseed1.binance.org/"
    }
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
}
