
from dataclasses import dataclass, field
from typing import Any, Dict
from library.MediatorMessageTypes import MediatorMessageTypes

import json

from library.TcpSocket import TcpSocket

VALIDATED_KEY = "validated"

@dataclass
class MediatorMessage:
    type: MediatorMessageTypes
    content: Dict[str, Any]

    @classmethod
    def fromStr(cls, string: str) -> "MediatorMessage":
        d = json.loads(string)
        return cls(MediatorMessageTypes.find_from_value(d["responseType"]), d)

    @classmethod
    def receive(cls, socket: TcpSocket) -> "MediatorMessage":
        return MediatorMessage.fromStr(socket.receive())

    def toJsonStr(self) -> str:
        return json.dumps(self.content)
