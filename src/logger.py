import logging
import json

logger = logging.getLogger("appLogger")
logging.basicConfig(level=logging.INFO, format="%(message)s")


class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        self.kwargs["msg"] = self.message
        return json.dumps(self.kwargs, default=str)


_ = StructuredMessage
