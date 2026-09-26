"""Fetch the newest unread customer email from a Gmail inbox over IMAP."""

import imaplib
import email
from email import policy
from email.message import Message
from email.utils import parseaddr


# Fill in the Gmail address associated with the App Password.
GMAIL_ADDRESS = "Eliteconquerorz@gmail.com"
GMAIL_APP_PASSWORD = "fdnvfgbfjwtdbxrc"


def _plain_text_body(message: Message) -> str:
    """Extract the plain-text body, ignoring attachments and HTML alternatives."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain" and part.get_content_disposition() != "attachment":
                content = part.get_content()
                if isinstance(content, str) and content.strip():
                    return content.strip()
        return ""

    if message.get_content_type() == "text/plain":
        content = message.get_content()
        return content.strip() if isinstance(content, str) else ""
    return ""


def fetch_latest_customer_email() -> dict[str, str] | None:
    """Return the newest unread email's body and sender, or None if inbox is clear."""
    mailbox = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    try:
        mailbox.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        status, _ = mailbox.select("INBOX")
        if status != "OK":
            raise RuntimeError("Could not open the Gmail inbox.")

        status, search_data = mailbox.search(None, "UNSEEN")
        if status != "OK":
            raise RuntimeError("Could not search for unread Gmail messages.")

        message_ids = search_data[0].split() if search_data and search_data[0] else []
        if not message_ids:
            return None

        latest_id = message_ids[-1]
        status, fetch_data = mailbox.fetch(latest_id, "(RFC822)")
        if status != "OK":
            raise RuntimeError("Could not fetch the latest unread email.")

        raw_message = next(
            (item[1] for item in fetch_data if isinstance(item, tuple) and len(item) > 1),
            None,
        )
        if raw_message is None:
            raise RuntimeError("Gmail returned an empty message.")

        parsed_message = email.message_from_bytes(raw_message, policy=policy.default)
        body = _plain_text_body(parsed_message)
        _, sender = parseaddr(parsed_message.get("From", ""))
        if not body or not sender:
            return None
        return {"body": body, "sender": sender}
    finally:
        try:
            mailbox.close()
        except imaplib.IMAP4.error:
            pass
        mailbox.logout()