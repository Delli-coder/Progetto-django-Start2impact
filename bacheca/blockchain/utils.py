from web3 import Web3


def send_transaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/dac28346be90481388d1e6567e305669'))
    address = '0x2fb988e56EaC8CeD5ECF81A6d472442eD230698c'
    privateKey = '0xae558b90da7928ad00bb77904135e7661661fc5d56b74128a28c5b2316652489'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
