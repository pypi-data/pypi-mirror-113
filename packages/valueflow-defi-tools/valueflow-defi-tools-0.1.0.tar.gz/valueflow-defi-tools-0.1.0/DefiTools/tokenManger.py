from DefiTools.sendToken import SendToken


class TokenManger(SendToken):
    def distribute_mainnet_token(self, from_address: str, from_address_pri_key: str, to_address_list: list):
        """
        一对多分发主网代币
        :param from_address: 发送地址
        :param from_address_pri_key: 发送地址私钥
        :param to_address_list: 接收地址公钥列表
        """
        if self.w3.isConnected():
            for to_address in to_address_list:
                self.send_token(to_address, from_address, from_address_pri_key)

    def distribute_smart_contract_token(self, from_address: str, from_address_pri_key: str, to_address_list: list,
                                        smart_contract_address: str,
                                        abi: list):
        """
        一对多分发智能合约代币
        :param from_address: 发送地址
        :param from_address_pri_key: 发送地址私钥
        :param to_address_list: 接收地址公钥列表
        :param smart_contract_address: 智能合约地址
        :param abi: 智能合约abi
        """
        if self.w3.isConnected():
            for to_address in to_address_list:
                self.send_contract_token(to_address, from_address, from_address_pri_key, smart_contract_address, abi)

    def withdraw_other_account_mainnet_token(self, account_dict: dict, to_address: str):
        """
        多对一全回多余账户的所有主网代币
        :param account_dict: 存储公私钥账户字典
        e.g. {'public_key': private_key',}
        :param to_address: 接收地址公钥
        """
        if self.w3.isConnected():
            for from_address, from_address_pri_key in account_dict.items():
                self.send_token(to_address, from_address, from_address_pri_key)

    def withdraw_other_account_smart_contract_token(self, to_address: str, account_dict: dict,
                                                    smart_contract_address: str,
                                                    abi: list):
        """
        多对一全回多余账户的所有智能合约代币
        :param to_address: 接收地址公钥
        :param account_dict: 存储公私钥账户字典
        e.g. {'public_key': private_key',}
        :param smart_contract_address: 智能合约地址
        :param abi: 智能合约ABI
        :return:
        """
        if self.w3.isConnected():
            for from_address, from_address_pri_key in account_dict.items():
                self.send_contract_token(to_address, from_address, from_address_pri_key, smart_contract_address, abi)
