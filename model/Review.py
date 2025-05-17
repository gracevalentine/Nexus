from model.Item import Item

class Review:
    def __init__(self, review_id: int, review_text: str, item: Item = None, reviewer=None):
        if item is not None and not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        self._review_id = review_id
        self._review_text = review_text
        self._item = item
        self._reviewer = reviewer

    @property
    def review_id(self):
        return self._review_id

    @review_id.setter
    def review_id(self, value):
        self._review_id = value

    @property
    def review_text(self):
        return self._review_text

    @review_text.setter
    def review_text(self, value):
        self._review_text = value

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value

    @property
    def reviewer(self):
        return self._reviewer

    @reviewer.setter
    def reviewer(self, value):
        self._reviewer = value
