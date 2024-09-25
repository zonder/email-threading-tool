## Introduction

This guide provides step-by-step instructions on how to set up and use the Email Threading Tool that sends emails via the Nylas API. The script reads configurations and email content from YAML files and supports email threading by managing "In-Reply-To" headers.

![Arc_tnA5g9Puwv](https://github.com/user-attachments/assets/c1da06e3-6a5c-41d5-8c74-d2547ead9158)


## Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed on your system.
- **Nylas Developer Account**: Sign up for a Nylas developer account to obtain API credentials.
- **Email Accounts**: Access to email accounts that will be used as senders.

## Installation Steps

### 1. Clone the Repository

First, clone the repository or download the script files into a directory on your machine.

```bash
git clone https://github.com/zonder/email-threading-tool.git
cd email-automation-script
```

### 2. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Up Nylas API Credentials

#### a. Sign Up for Nylas

- Go to [Nylas Developer Portal](https://developer.nylas.com/) and sign up for an account.

#### b. Create a Nylas Application

- Once logged in, create a new application to get your **Client Secret**.

#### c. Store Credentials in `.config` File

Create a file named `.config` in the root directory of your project with the following content:

```ini
[nylas]
client_secret = YOUR_NYLAS_CLIENT_SECRET
```

Replace `YOUR_NYLAS_CLIENT_SECRET` with the credentials from your Nylas application.

### 4. Authenticate Sender Email Accounts

For each email account you want to use as a sender, you need to authenticate it with Nylas to obtain an **GRANT_ID** (referred to as `grant_id` in the script).

#### a. Use Nylas Hosted Authentication

- Follow the [Nylas Hosted Authentication Guide](https://developer.nylas.com/docs/developer-tools/authentication/hosted-authentication/) to authenticate your email accounts.

- After successful authentication, you will receive an **GRANT_ID** for each account.

#### b. Store Sender Information in `senders.yaml`

Create a `senders.yaml` file in the directory with the following structure:

```yaml
sender_key1:
  email: 'sender1@example.com'
  name: 'Sender One'
  grant_id: 'GRANT_ID_1'

sender_key2:
  email: 'sender2@example.com'
  name: 'Sender Two'
  grant_id: 'GRANT_ID_2'

# Add more senders as needed
```

Replace:

- `'sender1@example.com'` with the sender's email address.
- `'Sender One'` with the sender's name.
- `'ACCESS_TOKEN_1'` with the grant_id obtained from Nylas for that email account.

### 5. Prepare the Email Content

Create an email content file in YAML format (e.g., `emails.yaml`). This file will contain the emails you want to send.

#### Example `emails.yaml`:

```yaml
- id: 'email1'
  from: 'sender_key1'
  to:
    - 'recipient_key1'
  subject: 'Welcome to Our Service'
  content: 'Hello, thank you for joining our service.'
  timestamp: '2023-10-01T12:00:00Z'

- id: 'email2'
  from: 'sender_key1'
  to:
    - 'recipient_key2'
  in_reply_to: 'email1'
  subject: 'Re: Welcome to Our Service'
  content: 'Glad to have you with us!'
  timestamp: '2023-10-01T12:05:00Z'

```

Notes:

- **`id`**: A unique identifier for the email. Used for threading.
- **`from`**: The sender key as defined in `senders.yaml`.
- **`to`**, **`cc`**, **`bcc`**: Lists of recipient keys. Recipients should also be defined in `senders.yaml` or handled accordingly.
- **`subject`**: The subject line of the email.
- **`content`**: The body of the email.
- **`timestamp`**: ISO 8601 formatted timestamp. Used for sorting emails chronologically.
- **`in_reply_to`**: If the email is a reply, specify the `id` of the email it's replying to.

### 6. Update Recipient Information

In your `senders.yaml` file, add entries for recipients if needed:

```yaml
recipient_key1:
  email: 'recipient1@example.com'
  name: 'Recipient One'

recipient_key2:
  email: 'recipient2@example.com'
  name: 'Recipient Two'

# No grant_id is needed for recipients unless they are also senders
```

### 8. Run the Script

You can run the script using default paths or specify custom paths.

#### a. Using Default Paths

If your files are named `.config`, `senders.yaml`, and `emails.yaml`, and are located in the root directory, simply run:

```bash
python main.py
```

#### b. Specifying Custom Paths

If your files are in different locations or have different names, use command-line arguments:

```bash
python main.py --config path/to/.config --senders path/to/senders.yaml --emails path/to/emails.yaml
```

#### c. Enable Verbose Output

To see more detailed logs during execution, use the `--verbose` flag:

```bash
python main.py --verbose
```

### 9. Verify Emails Are Sent

After running the script, check the sender email accounts to verify that the emails have been sent. Also, check the recipient inboxes to ensure they have received the emails.

## Command-Line Arguments Reference

- `--config`: Path to the Nylas API configuration file (default: `.config`).
- `--senders`: Path to the senders YAML file (default: `senders.yaml`).
- `--emails`: Path to the emails YAML file (default: `emails.yaml`).
- `--verbose`: Enable verbose output for detailed logging.

## Troubleshooting

- **Import Errors**: Ensure all dependencies are installed in your current environment. Activate your virtual environment if using one.
- **Incorrect Paths**: Verify that the file paths provided to the script are correct.
- **Authentication Errors**: Ensure that the Nylas API credentials and access tokens are correct and have not expired.
- **Missing Sender/Recipient Keys**: Check that all sender and recipient keys used in `emails.yaml` are defined in `senders.yaml`.

## Extending the Script

- **Adding Attachments**: To send attachments, modify the `Email` data class and the `prepare_and_send_email` method in `email_client.py` to include attachment handling.
- **Custom Email Fields**: You can add additional fields to the `Email` data class and update the YAML files accordingly.
- **Logging**: For more advanced logging, consider integrating Python's `logging` module.

## Security Considerations

- **Sensitive Data**: Do not commit `.config` files or any files containing API credentials or access tokens to version control systems like GitHub.
- **Access Tokens**: Treat access tokens as secrets. If they are compromised, revoke them immediately via the Nylas dashboard.

## Support and Contributions

- **Issues**: If you encounter problems, open an issue on the project's GitHub repository.
- **Contributions**: Contributions are welcome! Feel free to submit pull requests with improvements or bug fixes.

## Conclusion

This script automates sending emails using the Nylas API and supports email threading. By following this guide, you should be able to set up and use the script to send customized emails from multiple sender accounts.
