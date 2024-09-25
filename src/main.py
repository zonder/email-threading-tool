import argparse
import logging

from data_provider import DataProvider
from email_client import EmailClient

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Send emails using EmailClient.')

    parser.add_argument('--config', default='.config',
                        help='Path to the configuration file.')
    parser.add_argument('--senders', default='./content/senders/example.yaml',
                        help='Path to the senders YAML file.')
    parser.add_argument('--emails', default='./content/conversations/example.yaml',
                        help='Path to the emails YAML file.')

    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output.')

    args = parser.parse_args()
    if args.verbose:
        print(f"Using config: {args.config}")
        print(f"Using senders file: {args.senders}")
        print(f"Using emails file: {args.emails}")

    data_provider = DataProvider(args.senders)
    email_client = EmailClient(args.config, data_provider)

    logger.info(f"Sending emails from: {args.emails}")
    email_client.send_emails(args.emails)
