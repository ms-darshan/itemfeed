from config import settings as SETTINGS
from importlib import import_module

default_route = {
    "item": "/item",
    "variant": "/variant"
}

class CustomRuleRouter():
    def __init__(self):
        self.ROUTES = self.prepare_routes()

    def prepare_routes(self):
        global_rules = []
        for x in SETTINGS.INSTALLED_APPS:
            preArr = []
            if x in default_route:
                preArr = [default_route[x].strip("/")]
            r = import_module(".router", x)
            rules = map(lambda rule: ("/"+"/".join(preArr+rule[0].strip("/").split("/")), rule[1]), r.rules)
            global_rules += rules
        return global_rules
