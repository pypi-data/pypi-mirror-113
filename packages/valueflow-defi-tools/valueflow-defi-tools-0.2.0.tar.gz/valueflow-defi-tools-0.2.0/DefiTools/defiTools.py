from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
from abc import ABCMeta, abstractmethod
import requests
import json
import time
import asyncio
from DefiTools.params import evm_network, headers


class DefiTools(metaclass=ABCMeta):
    def __init__(self, network: str):
        """
        :param network: 使用的主网
        目前支持的主网：ethereum/polygon/fantom/binance-smart-chain
        """
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(evm_network[network]['rpcUrl']))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.chain_id = evm_network[network]['chainId']

    def get_gas(self, tx: dict) -> int:
        """
        计算消耗的gas
        :param tx: 传入的发送json
        :return: 估计算消耗的gas
        """
        gas = self.w3.eth.estimateGas(tx)
        return gas

    def get_gas_price(self, network: str) -> int:
        """
        获取当前的gas价格(使用Zapper API)
        :param network: 网络名称
        :return: 中等速度的gas价格
        """
        url = f'https://api.zapper.fi/v1/gas-price?api_key=5d1237c2-3840-4733-8e92-c5a58fe81b88&network={network}'
        while 1:
            try:
                res = requests.get(url, headers=headers)
            except Exception as e:
                pass
            else:
                break
        res = json.loads(res.content)['fast']
        return self.w3.toWei(res, 'gwei')

    def get_signature(self, pri_key: str, message: str) -> str:
        """
        离线消息签名
        :param message: 待签名信息
        :param pri_key: 私钥
        :return: 离线消息签名
        """
        message = encode_defunct(text=message)
        signature = self.w3.eth.account.sign_message(message, private_key=pri_key)
        signature = self.w3.toHex(signature.signature)
        return signature

    @staticmethod
    def convert_contract_token_to_ether(contract, contract_balance):
        """
        智能合约账户代币单位转换成ether（e.g. 单位：ether）
        :param contract: 智能合约ABI
        :param contract_balance: 智能合约代币余额
        :return: 转换单位后的合约余额
        """
        contract_decimals = contract.functions.decimals().call()
        decimals = 10 ** contract_decimals
        contract_balance = contract_balance / decimals
        return contract_balance

    @staticmethod
    def convert_contract_token_to_wei(contract, contract_balance):
        """
        智能合约账户代币单位转换成wei（e.g. 单位：ether）
        :param contract: 智能合约ABI
        :param contract_balance: 智能合约代币余额
        :return: 转换单位后的合约余额
        """
        contract_decimals = contract.functions.decimals().call()
        decimals = 10 ** contract_decimals
        contract_balance = contract_balance * decimals
        return contract_balance

    async def send_transaction(self, nonce: int, send_amount: int, to_address: str, from_address_pub_key: str,
                               from_address_pri_key: str, gas: int):
        """
        发送账户交易
        :param nonce: 账户nonce值
        :param from_address_pub_key: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        :param send_amount: 发送余额
        :param to_address: 接受地址
        :param gas: gas费用
        """
        transaction = {
            'to': to_address,
            'value': send_amount,
            'gas': gas,
            'gasPrice': self.get_gas_price(self.network),
            'nonce': nonce,
            'chainId': self.chain_id}
        signed_txn = self.w3.eth.account.sign_transaction(transaction, from_address_pri_key)
        await self.process_transaction(signed_txn, from_address_pub_key, to_address, nonce)

    async def send_contract_transaction(self, contract, send_amount: float, to_address: str, from_address_pub_key: str,
                                        from_address_pri_key: str, gas: int):
        """
        发送智能合约账户交易
        :param contract: 构建好的智能合约
        :param send_amount: 发送余额
        :param to_address: 接受地址
        :param from_address_pub_key: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        :param gas:
        :return:
        """
        nonce = self.w3.eth.get_transaction_count(from_address_pub_key)
        contract_txn = contract.functions.transfer(
            to_address,
            send_amount,
        ).buildTransaction({
            'chainId': self.chain_id,
            'gas': gas,
            'gasPrice': self.get_gas_price(self.network),
            'nonce': nonce,
        })
        signed_txn = self.w3.eth.account.sign_transaction(contract_txn, private_key=from_address_pri_key)
        await self.process_transaction(signed_txn, from_address_pub_key, to_address, nonce)

    async def send_tx_contract_transaction(self, nonce: int, from_address_pub_key: str, from_address_pri_key: str,
                                           to_address: str,
                                           send_amount: int, tx_data: str):
        """
        根据构建成的data发送合约交易
        :param nonce: nonce值
        :param from_address_pub_key: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        :param to_address: 接受地址
        :param send_amount: 发送余额
        :param tx_data: data值
        """
        gas = self.w3.eth.estimateGas({'to': to_address, 'data': tx_data})
        tx = {
            'chainId': self.chain_id,
            'nonce': nonce,
            'to': Web3.toChecksumAddress(to_address),
            'value': send_amount,
            'gas': gas,
            'gasPrice': self.get_gas_price(self.network),
            'data': f'{tx_data}'
        }
        sign_tx = self.w3.eth.account.sign_transaction(tx, from_address_pri_key)
        await self.process_transaction(sign_tx, from_address_pub_key, to_address, nonce)

    async def process_transaction(self, signed_txn, from_address: str, to_address: str, nonce: int):
        """
        处理交易过程，判断交易状态
        :param signed_txn: tx
        :param from_address: 发送地址
        :param to_address: 接受地址
        :param nonce: 账户nonce值
        """
        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_hash = self.w3.toHex(tx_hash)
        except ValueError:
            raise Exception(f"账号{from_address} 目前有笔交易正在进行")
        else:
            count_times = 0
            infura_network_url = {
                'ethereum': 'https://mainnet.infura.io/v3/2343217699c44b45851935789f1f89e6',
                'polygon': 'https://polygon-mainnet.infura.io/v3/2343217699c44b45851935789f1f89e6'
            }
            get_transaction_receipt_url = infura_network_url[self.network]
            transaction_receipt_data = {"jsonrpc": "2.0", "id": 2, "method": "eth_getTransactionReceipt",
                                        "params": [tx_hash]}
            session = requests.session()
            while 1:
                try:
                    res = json.loads(
                        session.post(get_transaction_receipt_url, headers=headers,
                                     data=json.dumps(transaction_receipt_data)).content)
                except Exception as e:
                    time.sleep(1)
                else:
                    if res['result'] or (count_times == 100):
                        break
                    await asyncio.sleep(3)
                    count_times += 1
            transaction_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
            if self.w3.eth.getTransactionCount(Web3.toChecksumAddress(from_address)) > nonce:
                if transaction_receipt.status == 1:
                    print(f"from:{from_address} to:{to_address} 代币发送成功")
                else:
                    raise Exception(f"from:{from_address} to:{to_address} 代币发送失败")
            else:
                raise Exception(f"当前网络拥堵,账号:{from_address} 发出的交易未被打包")


class SendTokenTools(DefiTools):
    @abstractmethod
    def send_token(self, sent_amount: int, to_address: str, from_address: str, from_address_pri_key: str):
        """
        发送主网代币
        :param sent_amount: 发送代币数量
        :param to_address: 接受地址
        :param from_address: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        """
        pass

    @abstractmethod
    def send_contract_token(self, send_amount: int, to_address: str, from_address: str, from_address_pri_key: str,
                            smart_contract_address: str,
                            abi: list):
        """
        发送智能合约代币
        :param send_amount: 发送代币数量
        :param to_address: 接收地址
        :param from_address: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        :param smart_contract_address: 智能合约地址
        :param abi: 智能合约abi
        """
        pass
