from flask import Flask, jsonify
import hashlib
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Create the blockchain and add a genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

@app.route('/get', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain:
        chain_data.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash
        })
    return jsonify({'chain': chain_data, 'length': len(chain_data)})

@app.route('/mine', methods=['GET'])
def mine():
    global previous_block  # Declare previous_block as a global variable
    new_data = f"Block #{len(blockchain) + 1} data"
    new_block = create_new_block(previous_block, new_data)
    blockchain.append(new_block)
    previous_block = new_block
    response = {
        'message': 'New block mined!',
        'index': new_block.index,
        'previous_hash': new_block.previous_hash,
        'timestamp': new_block.timestamp,
        'data': new_block.data,
        'hash': new_block.hash
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
# https://chat.openai.com/c/efd95615-88d4-499c-b763-ff339f97993b
