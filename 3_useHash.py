import datetime
import json
import hashlib

class Blockchain:
    def __init__(self):
        # เก็บกลุ่มของ Block
        self.chain = [] # List ที่เก็บ Block
        # Genesis Block
        self.create_block(nonce=1, previous_hash="0") # Genesis Block
        self.create_block(nonce=10, previous_hash="100") # Block สมมติขึ้นมา
       
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
    
# ใช้งาน Blockchain
blockchain = Blockchain()
# เข้ารหัส Block แรก
print(blockchain.hash(blockchain.chain[0]))
# เข้ารหัส Block สอง
print(blockchain.hash(blockchain.chain[1]))