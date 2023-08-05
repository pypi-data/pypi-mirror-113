import base64
import hashlib
import hmac


def base64_sha256(raw_data, raw_key=None):
    """
    Hashes a data first with the SHA256 algorithm, and then get's the BASE64 string.

    :param str raw_data: The data to be hashed.
    :param str raw_key: If present, will be used as jey of the hash.
    :return: The hashed and parsed string.
    :rtype: str
    """
    data = raw_data.encode("utf8")
    key = raw_key.encode("utf8") if raw_key else None
    if key:
        encoded_data = hmac.new(key.encode('utf8'), data.encode('utf8'), hashlib.sha256).digest()
    else:
        encoded_data = hashlib.sha256(data).digest()
    return (base64.b64encode(encoded_data)).decode("utf8")
