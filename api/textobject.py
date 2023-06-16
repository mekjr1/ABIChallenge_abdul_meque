class TextObject:
    def __init__(self, content, date, object_id):
        self.content = content
        self.date = date
        self.id = object_id
        self.sentiment = None

    def set_sentiment(self, sentiment):
        self.sentiment = sentiment

    def to_dict(self):
        return {
            'content': self.content,
            'date': self.date,
            'id': self.id,
            'sentiment': self.sentiment
        }