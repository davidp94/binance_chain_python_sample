import array
import base64
import binascii
import sys

import examples.dex_account_pb2 as dex_account_pb2

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.decoder import _DecodeVarint

from binance_chain import messages
from binance_chain.environment import BinanceEnvironment
from binance_chain.http import HttpApiClient
# from binance_chain.node_rpc.http import HttpRpcClient
from binance_chain.protobuf import dex_pb2
from binance_chain.utils import segwit_addr


def decode_tx(encoded_tx):
    encoded_msg = _extract_encoded_msg(encoded_tx)
    return _decode_msg(encoded_msg)

def get_addresses(decoded_msg):
    from_address = segwit_addr.encode("bnb", decoded_msg.inputs[0].address)
    to_address = segwit_addr.encode("bnb", decoded_msg.outputs[0].address)
    return from_address, to_address

def convert_to_hex_address(bnb_address):
    decoded_addr = segwit_addr.decode_address(bnb_address)
    return decoded_addr.hex().upper()

def convert_to_account_data(bnb_address):
    hex_address = convert_to_hex_address(bnb_address)
    return "0x6163636F756E743A" + hex_address

def decode_account_info(account_value):
    account_decoded = base64.b64decode(account_value)
    return dex_account_pb2.AppAccount().FromString(account_decoded[4:])

def extract_account_total_balance(account_info, denom):
    balance = 0
    for coin in account_info.base.coins:
        if coin.denom == denom:
            balance += coin.amount
            break
    for coin in account_info.locked:
        if coin.denom == denom:
            balance += coin.amount
    return balance / (10 ** 8)

def _extract_encoded_msg(encoded_tx):
    decoded = base64.b64decode(encoded_tx)
    msg_len, new_pos = _DecodeVarint(decoded, 0)
    tx_type = decoded[new_pos:new_pos+4]

    stdtx_pb2 = dex_pb2.StdTx().FromString(decoded[new_pos+4:])
    return stdtx_pb2.msgs[0]

def _decode_msg(msg_bytes: bytes) -> dex_pb2.StdTx:
    msg_type = msg_bytes[:4]
    msg_class = _amino_msg_type_to_class(msg_type)
    msg_pb2 = msg_class().FromString(msg_bytes[4:])
    return msg_type.hex().upper(), msg_pb2 

def _amino_msg_type_to_class(msg_type: bytes):
    return {
            messages.NewOrderMsg.AMINO_MESSAGE_TYPE: dex_pb2.NewOrder,
            messages.CancelOrderMsg.AMINO_MESSAGE_TYPE: dex_pb2.CancelOrder,
            messages.FreezeMsg.AMINO_MESSAGE_TYPE: dex_pb2.TokenFreeze,
            messages.UnFreezeMsg.AMINO_MESSAGE_TYPE: dex_pb2.TokenUnfreeze,
            messages.TransferMsg.AMINO_MESSAGE_TYPE: dex_pb2.Send,
            # messages.VoteMsg.AMINO_MESSAGE_TYPE: dex_pb2.Vote,
    }.get(binascii.hexlify(msg_type).upper())
