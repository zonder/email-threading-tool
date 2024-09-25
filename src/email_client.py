import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List

from dateutil import parser
from nylas import Client

import utils
from data_provider import DataProvider
from models.email import Email

TIMEOUT = 60
FETCH_TIMEOUT_IN_SECONDS = 2


class EmailClient:
    def __init__(self, config_file: str, data_provider: DataProvider):
        self.client_secret = utils.load_config(config_file)
        self.data_provider = data_provider

        self.nylas_client = Client(self.client_secret)

        self.message_id_map_rfc: Dict[str, str] = {}
        self.message_id_map_nylas: Dict[str, str] = {}
        self.logger = logging.getLogger(__name__)

    def sort_emails_by_timestamp(self, emails: List[Email]) -> List[Email]:
        def get_timestamp(email: Email) -> datetime:
            if email.timestamp:
                return parser.parse(email.timestamp)
            else:
                return datetime.min

        return sorted(emails, key=get_timestamp)

    def fetch_parent_rfc_message_id(self, grant_id, parent_email_from, in_reply_to_rfc):
        start_time = time.time()

        now = datetime.utcnow()
        query_time_unix = int((now - timedelta(minutes=1)).timestamp())
        while True:

            self.logger.info(
                f"Fetching parent message id: {grant_id} - {parent_email_from} - {in_reply_to_rfc}")

            incoming_messages = self.nylas_client.messages.list(grant_id, query_params={
                'from': parent_email_from,
                "fields": "include_headers",
                "received_after": query_time_unix,
                "limit": 20
            }).data

            for message in incoming_messages:
                parent_rfc_message_id = next(
                    (header.value for header in message.headers if header.name.lower()
                     == 'message-id'), None
                )

                if parent_rfc_message_id == in_reply_to_rfc:
                    return message.id

            if time.time() - start_time > TIMEOUT:
                self.logger.error(
                    "Timeout reached while fetching parent message ID")
                raise TimeoutError(
                    "Failed to fetch parent message ID within the timeout period.")

            time.sleep(FETCH_TIMEOUT_IN_SECONDS)

    def prepare_and_send_email(self, email: Email, sorted_emails: List[Email]) -> None:

        email_id = email.id
        sender_key = email.from_
        sender_info = self.data_provider.get_sender(sender_key)

        recipients = {
            "to": self.data_provider.get_recipients(email.to),
            "cc": self.data_provider.get_recipients(email.cc),
            "bcc": self.data_provider.get_recipients(email.bcc)
        }

        from_email = sender_info.email
        from_name = sender_info.name

        in_reply_to = None
        if email.in_reply_to:
            parent_id = email.in_reply_to
            in_reply_to_rfc = self.message_id_map_rfc.get(parent_id)
            parent_email = next(
                (e for e in sorted_emails if e.id == parent_id), None)
            if parent_email and in_reply_to_rfc:
                parent_email_from = self.data_provider.get_sender(
                    parent_email.from_).email
                in_reply_to = self.fetch_parent_rfc_message_id(
                    sender_info.grant_id, parent_email_from, in_reply_to_rfc
                )

        message_data = {
            "from": [{"name": from_name, "email": from_email}],
            "to": recipients["to"],
            "cc": recipients["cc"],
            "bcc": recipients["bcc"],
            "subject": email.subject,
            "body": email.content,
            "reply_to_message_id": in_reply_to,
            "headers": {"thread_timestamp": datetime.utcnow().isoformat()}
        }
        try:
            message = self.nylas_client.messages.send(
                sender_info.grant_id, message_data)

            saved_headers = self.nylas_client.messages.find(sender_info.grant_id, message.data.id, query_params={
                "fields": "include_headers"}).data.headers

            saved_message_id = next(
                (header.value for header in saved_headers if header.name.lower()
                 == 'message-id'), None)

            self.message_id_map_rfc[email_id] = saved_message_id
            self.message_id_map_nylas[email_id] = message.data.id

            self.logger.info(
                f"Sent email ID: {email_id} with Message-ID: {saved_message_id}")
        except Exception as e:
            self.logger.error(
                f"Failed to send email ID: {email_id}. Error: {str(e)}")

    def send_emails(self, file_name: str) -> None:
        emails = self.data_provider.load_emails(file_name)

        sorted_emails = self.sort_emails_by_timestamp(emails)

        for email in sorted_emails:
            self.prepare_and_send_email(email, sorted_emails)
