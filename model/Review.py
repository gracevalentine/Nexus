from model.Item import Item

class Review:
    def __init__(self, review_id: int, review_text: str, item: Item = None, reviewer=None):
        if item is not None and not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        self.review_id = review_id
        self.review_text = review_text
        self.item = item
        self.reviewer = reviewer

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
    
    def get_reviewer(self):
        return self.reviewer
    
    def set_reviewer(self, reviewer):
        self.reviewer = reviewer