from Crypto.Cipher import AES
import base64


class EncryptionService:
    _key = b'Sixteen byte key' 

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())

        encrypted_data = cipher.nonce + tag + ciphertext
        return base64.urlsafe_b64encode(encrypted_data).decode().rstrip("=")

    def decrypt(self, encrypted_data: str) -> str:
        try:
            padded_encrypted_data = encrypted_data + '=' * (-len(encrypted_data) % 4)
            encrypted_bytes = base64.urlsafe_b64decode(padded_encrypted_data)

            nonce = encrypted_bytes[:16]
            tag = encrypted_bytes[16:32]
            ciphertext = encrypted_bytes[32:]

            cipher = AES.new(self._key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode()
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None
