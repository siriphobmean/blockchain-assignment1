import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        # เก็บกลุ่มของ Block
        self.chain = [] # List ที่เก็บ Block
        # Genesis Block
        self.create_block(nonce=1, previous_hash="0") # Genesis Block
        self.create_block(nonce=10, previous_hash="00")
        self.create_block(nonce=20, previous_hash="000")
       
    # สร้าง Block ขึ้นมาในระบบ Blockchain   
    def create_block(self, nonce, previous_hash):
        # เก็บส่วนประกอบของ Block แต่ละ Block
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
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
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

# Run Server
if __name__ =="__main__":
    app.run()
    
