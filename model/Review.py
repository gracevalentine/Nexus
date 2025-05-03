from model import Item

class review:
    def __init__(self, review_id, review_text, item = Item.none):
        self.review_id = review_id
        self.review_text = review_text
        self.item = item

    def get_review_id(self):
        return self.review_id
    
    def set_review_id(self, review_id: int):
        self.review_id = review_id         
        
    def get_review_text(self):
        return self.review_text     
    
    def set_review_text(self, review_text: str):
        self.review_text = review_text  
        
    def get_item(self):
        return self.item    
    
    def set_item(self, item: Item):
        self.item = item