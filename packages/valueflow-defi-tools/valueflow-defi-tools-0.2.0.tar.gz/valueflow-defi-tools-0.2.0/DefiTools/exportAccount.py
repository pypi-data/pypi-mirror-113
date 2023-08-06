from eth_account import Account
import yaml
import os


def create_account(num: int) -> dict:
    """
    创建账户
    :param num: 生成的账户数量
    :return: 生成的账户列表 {公钥: 私钥}
    """
    account_dict = {}
    for i in range(num):
        acc = Account.create()
        pub_key = acc.address
        pri_key = acc.key.hex()
        if pub_key not in account_dict:
            account_dict[pub_key] = pri_key
    return account_dict


def export_account(filename: str, num: int):
    """
    导出账户
    :param filename: 存放的文件名
    :param num: 生成的账户数量
    """
    create_account_dict = create_account(num)
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                account_dict = config['DEFAULT']['ACCOUNT_MESSAGE']
                account_message = dict(account_dict, **create_account_dict) if account_dict else create_account_dict
                write_yaml(filename, account_message)
        except TypeError:
            write_yaml(filename, create_account_dict)
    else:
        write_yaml(filename, create_account_dict)


def write_yaml(filename: str, account_message: dict):
    """
    按设定好的格式写入 yml 文件
    :param filename: 文件名
    :param account_message: 公私钥存放的字典
    """
    desired_caps = {
        'DEFAULT': {
            'ACCOUNT_MESSAGE': account_message
        }
    }
    with open(f'{filename}', 'w', encoding="utf-8") as f:
        yaml.dump(desired_caps, f)
