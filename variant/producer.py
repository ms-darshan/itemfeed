from lib.producer import Producer

class VariantFeedGeneration(Producer):
    topic = "variant_feed"

    def __init__(self, topic=None):
        super(VariantFeedGeneration, self).__init__(topic)
    
    def transform(self, data):
        return {"variant": data}
