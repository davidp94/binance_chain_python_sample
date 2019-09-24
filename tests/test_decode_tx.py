import sys
import os
import requests
import json

parent_directory = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(parent_directory)
sys.path.append(parent_directory+'/examples')

from examples import decode_tx
from examples import dex_account_pb2


if __name__ == "__main__":
    txs = [
        "xQHwYl3uCkwqLIf6CiIKFBfeDAE1Xd8LQ4CjSsv6LHAaWQWnEgoKA0JOQhD67+UGEiIKFBfeDAE1Xd8LQ4CjSsv6LHAaWQWnEgoKA0JOQhD67+UGEnEKJuta6YchA/qw8WAGFELktqI1NXDsYK9sMp61T3UElWjgTBkmEyWqEkBhdJhl4wZLLjyhmkcKFkfL8vpFmiEfVejZgNX/tcdmZjuhCQUvZql85K++MQS+1C8qcZ+YSAgdU5bgX7mZyTnUGK6tBiCCAg==",
        "4wHwYl3uCmjObcBDChR+NoVC8WSqtpuzHENnYAtG+wFJFBIuN0UzNjg1NDJGMTY0QUFCNjlCQjMxQzQzNjc2MDBCNDZGQjAxNDkxNC0xODU0OBoLUEhCLTJERl9CTkIgAigBMJusBTiAgJPotRVAARJxCibrWumHIQIO+XNEPzoixFyv5bUDgbweD5e+EjSFGwX//GAJFZD6WxJAcWgjCaBpxQv2UyLY6YZ4Wlfx15Gef8tmDmvAVRhOIiVIC42szyer9pDN0V++btg/rC+Jkwq/O9enOE+fNGlF3xitYCDzkAEgAw==",
        "4wHwYl3uCmjObcBDChTEji7BGx0OHFcQP/JQDSQtYg02XRIuQzQ4RTJFQzExQjFEMEUxQzU3MTAzRkYyNTAwRDI0MkQ2MjBEMzY1RC0xODA3NBoLUEhCLTJERl9CTkIgAigBMLO8BTiA0JCL3xJAARJxCibrWumHIQNUw+T33B4h3E01t9QXuQbcU5YmhaiKdo3us7VAiCNMmBJAxn7WNtJKq5C97m96oFS5NVzuTNsk8Gfuk+e7g7l8prBDEYqrlwq4wUb8WswzpPaiV44mmfCpNnP35y21FBmKPxirYCCZjQEgAw==",
        "0wHwYl3uCk4qLIf6CiMKFJGTdSD0BFj1tBTSZ5YbRsGXid1wEgsKA0JOQhDgj/WsAxIjChSOpw19LqihS6KzPRjV371vrgpuqBILCgNCTkIQ4I/1rAMScAom61rphyEDVuClgDiab9LMkc1SXG1aTYBUr3DfF0hOWGePn1dKC00SQKstbRg7fwGp4DZbIgJx1NDinXG//SgjbAzXiWmXp5nbGZ5hxUnFReCTqeGyw9AbnHRRT7VW47k+zxF8PDn2cEIYMyD39AEaCTEwNTUyNDAwMCAC"
    ]

    for tx in txs:
        msg_type, msg = decode_tx.decode_tx(tx)
        # print(msg)

        if msg_type == "2A2C87FA":
            from_addr, to_addr = decode_tx.get_addresses(msg)

            addrs = [from_addr, to_addr]
            for addr in addrs:
                account_data = decode_tx.convert_to_account_data(addr)
                r = requests.get('https://dataseed5.defibit.io/abci_query?path="/store/acc/key"&data=' + account_data)
                result = json.loads(r.text)

                account_info = decode_tx.decode_account_info(result['result']['response']['value'])
                balance = decode_tx.extract_account_total_balance(account_info, "BNB")
                print(f'{addr} total balance : {balance}')

    