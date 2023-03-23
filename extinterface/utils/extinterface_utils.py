import base64
import hmac
import hashlib


def generate_signature(webhook_key, signed_data):
    """Generates a base64-encoded signature.

    Parameters:
    webhook_key (bytes object): utf-8 encoded webhook auth key
    signed_data (string): data to create signature

    Returns:
    string: A base64 encoded and hashed string
    """

    return base64.b64encode(
        hmac.new(webhook_key, msg=signed_data.encode("utf-8"), digestmod=hashlib.sha1).digest()).decode()
