from . import handlers

rules = [
        ("/insert", handlers.InsertItemHandler),
        ("/update", handlers.UpdateItemHandler),
        ("/delete", handlers.DeleteItemHandler),
]
