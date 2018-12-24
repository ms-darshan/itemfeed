from . import handlers

rules = [
    ("/insert", handlers.InsertVariantHandler),
    ("/update", handlers.UpdateVariantHandler),
    ("/delete", handlers.DeleteVariantHandler),
]
