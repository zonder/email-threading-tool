from dataclasses import dataclass


@dataclass
class Sender:
    email: str
    name: str
    grant_id: str
