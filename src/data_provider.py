import logging
from typing import Dict, List

import utils
from models.email import Email
from models.sender import Sender


class DataProvider:
    def __init__(self, senders_file: str):
        self.senders: Dict[str, Sender] = self._load_senders(
            senders_file)
        self.logger = logging.getLogger(__name__)

    def _load_senders(self, senders_file) -> Dict[str, Sender]:
        senders_data = utils.load_yaml(senders_file)
        senders = {}
        for key, data in senders_data.items():
            senders[key] = Sender(
                email=data['email'],
                name=data['name'],
                grant_id=data['grant_id']
            )
        return senders

    def load_emails(self, file_name: str) -> List[Email]:
        emails_data = utils.load_yaml(file_name)
        emails = []
        for email_data in emails_data:
            email = Email(
                id=email_data['id'],
                from_=email_data['from'],
                to=email_data.get('to', []),
                cc=email_data.get('cc', []),
                bcc=email_data.get('bcc', []),
                subject=email_data['subject'],
                content=email_data['content'],
                timestamp=email_data.get('timestamp'),
                in_reply_to=email_data.get('in_reply_to')
            )
            emails.append(email)
        return emails

    def get_sender(self, sender_key: str) -> Sender:
        return self.senders.get(sender_key)

    def get_recipients(self, recipient_keys: List[str]) -> List[Dict[str, str]]:
        recipients = []
        for r in recipient_keys:
            sender = self.senders.get(r)
            if sender:
                recipients.append({'email': sender.email, 'name': sender.name})
            else:
                print(f"Sender key '{r}' not found in senders")
        return recipients
