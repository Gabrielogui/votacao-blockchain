import hashlib
import json
from time import time

from cryptography.fernet import Fernet


'''key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)'''

with open("key.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # dicionário com os dados do voto
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time(), {"message": "Genesis Block"}, "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True