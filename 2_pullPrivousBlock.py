import datetime

class Blockchain:
    def __init__(self):
        # เก็บกลุ่มของ Block
        self.chain = [] # List ที่เก็บ Block
        # Genesis Block
        self.create_block(nonce=1, previous_hash="0")
        self.create_block(nonce=10, previous_hash="10")
        self.create_block(nonce=30, previous_hash="20")
       
    # สร้าง Block ขึ้นมาในระบบ Blockchain   
    def create_block(self, nonce, previous_hash):
        # เก็บส่วนประกอบของ Block แต่ละ Block
        block = {
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "previous_hash":previous_hash
        }
        self.chain.append(block)
        return block
    
    # ให้บริการเกี่ยวกับ Block ก่อนหน้า
    def get_previous_block(self):
        return self.chain[-1]
    
# ใช้งาน Blockchain
blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.get_previous_block)