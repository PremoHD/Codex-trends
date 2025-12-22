import hashlib
import time

class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_block()

    def hash_block(self):
        s = f"{self.index}{self.timestamp}{self.data}{self.prev_hash}"
        return hashlib.sha256(s.encode()).hexdigest()

class CommunityChain:
    def __init__(self):
        self.chain = [Block(0, "Genesis", "0")]

    def add_record(self, data):
        last = self.chain[-1]
        self.chain.append(Block(len(self.chain), data, last.hash))