import base64
import io
import rsa
import rsa.pkcs1


PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(io.open("py/server/security/private-key.pem", "rb").read(), "PEM")


def decryptText(ciphertext):
    """
    Decrypts the ciphertext.

    :param ciphertext: RSA encrypted text.
    :return: Decrypted text. If error return empty string.
    """
    try:
        return rsa.decrypt(base64.b64decode(ciphertext.encode("utf-8")), PRIVATE_KEY).decode("utf-8")
    except rsa.pkcs1.DecryptionError:
        return ""
    except UnicodeDecodeError:
        return ""
