import datetime
import json
import hashlib
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        # เก็บกลุ่มของ Block
        self.chain = [] # List ที่เก็บ Block
        self.year = 2020
        self.generated_blocks = False
        # Genesis Block
        self.create_block(nonce=1, previous_hash="0") # Genesis Block
       
    # สร้าง Block ขึ้นมาในระบบ Blockchain   
    def create_block(self, nonce, previous_hash):
        # เก็บส่วนประกอบของ Block แต่ละ Block
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "data": self.year,
            "previous_hash": previous_hash
        }
        block["hash"] = self.hash(block)
        self.chain.append(block)
        return block
    
    # ให้บริการเกี่ยวกับ Block ก่อนหน้า
    def get_previous_block(self):
        return self.chain[-1]
    
    # เข้ารหัส Block
    def hash(self, block):
        # แปลง Python Object (dict) -> json Object (ยังไม่ได้ hash)
        encode_block = json.dumps(block, sort_keys=True).encode()
        # กำหนดรูปแบบ SHA-256 ได้กลุ่มเลขฐาน 16
        return hashlib.sha256(encode_block).hexdigest()
    
    def proof_of_work(self, previous_nonce):
        # อยากได้ค่า Nonce = ??? ที่ส่งผลให้ได้ Target Hash -> 4 หลักแรกเป็น 0000xxxxxxxxxx
        new_nonce = 1 # ค่า Nonce ที่ต้องการ
        check_proof = False # ตัวแปรที่เช็คค่า Nonce ให้ได้ตาม Target ที่กำหนด
        
        # แก้โจทย์ทางคณิตศาสตร์
        while check_proof is False:
            # ได้เลขฐาน 16 มา 1 ชุด
            hashoperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce 
    
    # ตรวจสอบ Block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] # Block ที่ตรวจสอบ
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"] # Nonce Block ก่อนหน้า
            nonce = block["nonce"] # Nonce ของ Block ที่ตรวจสอบ
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True
    
# Web Server
app = Flask(__name__)
    
# ใช้งาน Blockchain
blockchain = Blockchain()

# Routing
@app.route('/')
def hello():
    return "<h1>Hello Blockchain</h1>"

@app.route('/get_chain', methods=["GET"])
def get_chain():
    if not blockchain.generated_blocks:
        # กระทำเฉพาะครั้งแรกเท่านั้น
        num_blocks = int(request.args.get('num_blocks', 10))
        for i in range(1, num_blocks + 1):
            previous_block = blockchain.get_previous_block()
            previous_nonce = previous_block["nonce"]
            nonce = blockchain.proof_of_work(previous_nonce)
            previous_hash = blockchain.hash(previous_block)
            block = blockchain.create_block(nonce, previous_hash)
            block["data"] = 2020 + i
            blockchain.chain[-1] = block

        blockchain.generated_blocks = True  # ตั้งค่าให้มีการสร้าง block แล้ว

    response = {
        "message": "Generated blocks successfully",
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    for block in blockchain.chain:
        block["hash"] = blockchain.hash(block)
    return jsonify(response), 200

@app.route('/mining', methods=["GET"])
def mining_block():
    amount = 1
    blockchain.year = blockchain.year+amount
    # PoW
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    # หาค่า Nonce ที่เหมาะสม
    nonce = blockchain.proof_of_work(previous_nonce)
    # หา Hash ของ Block ก่อนหน้ามาใช้งาน
    previous_hash = blockchain.hash(previous_block)
    # Update Block ใหม่
    block = blockchain.create_block(nonce, previous_hash)
    # เพิ่ม hash ของ block ที่ถูกขุดใน response
    block["hash"] = blockchain.hash(block)
    response = {
        "message": "Mining Block เรียบร้อย",
        "index":  block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"],
        "hash": block["hash"]  # เพิ่ม hash ของ block ใน response
    }
    return jsonify(response), 200

@app.route('/mine_new', methods=["GET"])
def mine_new_block():
    if not blockchain.generated_blocks:
        # สร้าง 10 บล็อกแรก
        num_blocks = 10
        for i in range(1, num_blocks + 1):
            previous_block = blockchain.get_previous_block()
            previous_nonce = previous_block["nonce"]
            nonce = blockchain.proof_of_work(previous_nonce)
            previous_hash = blockchain.hash(previous_block)
            block = blockchain.create_block(nonce, previous_hash)
            block["data"] = 2020 + i
            blockchain.chain[-1] = block

        blockchain.generated_blocks = True  # ตั้งค่าเป็น True หลังจากสร้างบล็อกแล้ว

    # ใช้ค่า year จาก block ล่าสุดใน 10 บล็อก
    latest_block_year = blockchain.chain[-1]["data"]

    # ขุดบล็อกใหม่โดยเพิ่มค่า year
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)
    block["data"] = latest_block_year + 1  # เพิ่มค่า year
    blockchain.chain[-1] = block

    response = {
        "index":  block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"],
        "hash": block["hash"]
    }

    return jsonify(response), 200

@app.route('/is_valid', methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            "message": "Blockchain is Valid",
            "hashes": [blockchain.hash(block) for block in blockchain.chain]  # เพิ่ม hash ของแต่ละ block ใน response
            }
    else:
        response = {"message": "Have Problem, Blockchain Is not Valid"}
    return jsonify(response), 200

# Run Server
if __name__ =="__main__":
    app.run()