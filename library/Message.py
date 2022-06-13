
from dataclasses import dataclass, field
from typing import Any, Dict

from library.MessageTypes import MessageTypes

import json

VALIDATED_KEY = "validated"

@dataclass
class Message:
    type: MessageTypes
    content: Dict[str, Any]

    @classmethod
    def fromStr(cls, string: str) -> "Message":
        d = json.loads(string)
        return cls(MessageTypes.find_from_value(d["type"]), d["content"])

    def toJsonStr(self) -> str:
        d = {
            "type": self.type.value,
            "content": self.content
        }
        return json.dumps(d)

    def is_validated(self) -> bool:
        """ Check if the message have the "validated" field 
        and if this field is set tot True
        """
        if VALIDATED_KEY in self.content:
            return self.content[VALIDATED_KEY]
        return False

    def assert_validated(self) -> None:
        """Check if the message have the "validated" field 
        and if this field is set tot True, else raise an exception
        """
        if not self.is_validated():
            raise ValueError(f"Message with content not validated : {self.content}")