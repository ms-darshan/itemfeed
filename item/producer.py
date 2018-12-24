from lib.producer import Producer

class ItemFeedGeneration(Producer):
    topic = "item_feed"
    
    def __init__(self, topic=None):
        super(ItemFeedGeneration, self).__init__(topic)

    def transform(self, data):
        return { "item": data }
