from DefiTools.defiTools import SendTokenTools
from web3 import Web3


class SendToken(SendTokenTools):

    async def send_token(self, send_amount: int, to_address: str, from_address: str, from_address_pri_key: str):
        """
        发送主网代币
        :param send_amount: 发送代币数量
        :param to_address: 接受地址
        :param from_address: 发送地址的公钥
        :param from_address_pri_key: 发送地址的私钥
        """
        nonce = self.w3.eth.getTransactionCount(from_address)
        balance = self.w3.eth.get_balance(from_address)
        gas = self.get_gas({'from': from_address, 'to': to_address, 'value': balance})
        gas_price = self.get_gas_price(self.network)
        if send_amount == 0:
            send_amount = balance - (gas * gas_price)
            if send_amount > 0:
                await self.send_transaction(nonce, send_amount, to_address, from_address, from_address_pri_key, gas)
        else:
            balance = balance - send_amount - (gas * gas_price)
            if balance > 0:
                await self.send_transaction(nonce, send_amount, to_address, from_address, from_address_pri_key, gas)

    async def send_contract_token(self, send_amount: float, to_address: str, from_address: str,
                                  from_address_pri_key: str,
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
        contract_address = Web3.toChecksumAddress(smart_contract_address)
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        send_amount = self.convert_contract_token_to_wei(contract, send_amount)
        balance = self.w3.eth.get_balance(from_address)
        contract_balance = contract.functions.balanceOf(from_address).call()
        if contract_balance > 0 and balance > 0:
            data = contract.encodeABI(fn_name="transfer", args=[to_address,
                                                                contract_balance])
            gas = self.w3.eth.estimateGas({'to': to_address, 'data': data}) * 3
            gas_payable = balance - (gas * self.get_gas_price(self.network))
            if gas_payable >= 0:
                if send_amount == 0:
                    await self.send_contract_transaction(contract, contract_balance, to_address, from_address,
                                                         from_address_pri_key, gas)
                else:
                    if contract_balance - send_amount >= 0:
                        await self.send_contract_transaction(contract, send_amount, to_address, from_address,
                                                             from_address_pri_key, gas)
