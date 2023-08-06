import random
import string

from asn1crypto import cms

CONTENT_ENCRYPTION_ALGORITHM = "aes256_cbc"

def generate_random_password() -> str:
    """ Generate random password from letters and digits

        Raises:
            UserCredentialsError: If credentials files are not found
        Returns:
            String: Random string password
    """
    dictionary = string.ascii_letters + string.digits
    password_length = random.randint(10, 15)
    return ''.join(random.choice(dictionary) for _ in range(password_length))


def encrypt_data(data):
    eci = cms.EncryptedContentInfo({
        "content_type": "data",
        "content_encryption_algorithm": {
            "algorithm": CONTENT_ENCRYPTION_ALGORITHM,
            "parameters": bytes.fromhex(self._symmetric_iv)
        },
        "encrypted_content": encrypted_data
    })
