from DefiTools.defiTools import SendTokenTools
from web3 import Web3


class SendToken(SendTokenTools):

    def send_token(self, to_address: str, from_address: str, from_address_pri_key: str):
        """
        发送主网代币
        :param to_address: 接受地址
        :param from_address: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        """
        nonce = self.w3.eth.getTransactionCount(from_address)
        balance = self.w3.eth.get_balance(from_address)
        balance = self.w3.toWei(balance, 'ether')
        gas = self.get_gas({'from': from_address, 'to': to_address, 'value': 1})
        send_amount = balance - (gas * self.get_gas_price(self.network))
        if send_amount > 0:
            self.send_transaction(nonce, send_amount, to_address, from_address, from_address_pri_key, gas)

    def send_contract_token(self, to_address: str, from_address: str, from_address_pri_key: str,
                            smart_contract_address: str,
                            abi: list):
        """
        发送智能合约代币
        :param to_address: 接收地址
        :param from_address: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        :param smart_contract_address: 智能合约地址
        :param abi: 智能合约abi
        """
        contract_address = Web3.toChecksumAddress(smart_contract_address)
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        balance = self.w3.eth.get_balance(from_address)
        balance = self.w3.toWei(balance, 'ether')
        contract_balance = contract.functions.balanceOf(from_address).call()
        data = contract.encodeABI(fn_name="transfer", args=[to_address,
                                                            contract_balance])
        gas = self.w3.eth.estimateGas({'to': to_address, 'data': data})
        gas_payable = balance - (gas * self.get_gas_price(self.network))
        if (gas_payable >= 0) and (contract_balance > 0):
            self.send_contract_transaction(contract, contract_balance, to_address, from_address,
                                           from_address_pri_key, gas)
