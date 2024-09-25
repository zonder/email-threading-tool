from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Email:
    id: str
    from_: str
    to: List[str]
    subject: str
    content: str
    timestamp: Optional[str] = None
    in_reply_to: Optional[str] = None
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
