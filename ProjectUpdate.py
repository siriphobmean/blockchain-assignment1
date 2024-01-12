import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        # เก็บกลุ่มของ Block
        self.chain = [] # List ที่เก็บ Block
        self.transaction = 0 # จำนวนเงิน # Step 9
        # Genesis Block
        self.create_block(nonce = 1, previous_hash = "0") # Genesis Block
        
    # 1 Create Genesis Block
    # สร้าง Block ขึ้นมาในระบบ Blockchain
    def create_block(self, nonce, previous_hash, hash):
        # เก็บส่วนประกอบของ Block แต่ละ Block
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "data": self.transaction, # ข้อมูลการทำธุรกรรม # Step 9
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block
    
    # 2 Pull Previous Block
    # ให้บริการเกี่ยวกับ Block ก่อนหน้า
    def get_previous_block(self):
        return self.chain[-1]
    
    # 3 Use Hash
    # เข้ารหัส Block
    def hash(self, block):
        # แปลง Python Object (dict) -> json Object (ยังไม่ได้ Hash)
        encode_block = json.dumps(block, sort_keys = True).encode()
        # กำหนดรูปแบบ SHA-256 ได้กลุ่มเลขฐาน 16
        return hashlib.sha256(encode_block).hexdigest()
    
    # 4 Search Nonce with Proof of Work (PoW)
    def proof_of_work(self, previous_nonce):
        # อยากได้ค่า Nonce = ? ที่ส่งผลให้ได้ Target Hash -> 4 หลักแรก 0000xxxxxxxxxx
        new_nonce = 1 # ค่า Nonce ที่ต้องการ
        check_proof = False # ตัวแปรที่เซ็ตค่า Nonce ให้ได้ตาม Target ที่กำหนด
        
        # แก้โจทย์ทางคณิตศาสตร์
        while check_proof is False:
            # ได้เลขฐาน 16 มา 1 ชุด
            hashOperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashOperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce
    
    # 8 Verify Blockchain
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] # Block ที่ตรวจสอบ
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"] # Nonce Block ก่อนหน้า
            nonce = block["nonce"] # Nonce ของ Block ที่ตรวจสอบ
            hashOperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashOperation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

# 5 Add Flask Framework
# Web Server    
app = Flask(__name__)

# ใช้งาน Blockchain
blockchain = Blockchain()

# Routing
@app.route('/')
def hello():
    return "<h1>Hello Blockchain</h1>"

# 6 Pull All Block
@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

# 7 Make Mining Block
@app.route('/mining', methods=["GET"])
def mining_block():
    # Proof of Work
    amount = 1000000 # จำนวนเงินในการทำธุรกรรมแต่ละครั้ง # Step 9
    blockchain.transaction = blockchain.transaction+amount # Step 9
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    # หาค่า Nonce ที่เหมาะสม
    nonce = blockchain.proof_of_work(previous_nonce)
    # หา Hash ของ Block ก่อนหน้ามาใช้งาน
    previous_hash = blockchain.hash(previous_block)
    # Update Block ใหม่
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        "message": "Mining Block Success",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "data": block["data"],
        "hash": blockchain.hash(block), # Hash ของ Block ที่ถูกขุด (Update)
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200

# 8 Verify Blockchain
@app.route('/is_valid', methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "Blockchain is Valid!"}
    else:
        response = {"message": "Have Problem, Blockchain is not Valid!"}
    return jsonify(response), 200

# Run Server
if __name__ == "__main__":
    app.run()