from Crypto.Cipher import AES
import base64

class EncryptionService:
    _key = b'Sixteen byte key' 

    def __encrypt_ballot_id(self, data: str) -> str:
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())

        encrypted_data = cipher.nonce + tag + ciphertext
        return base64.urlsafe_b64encode(encrypted_data).decode().rstrip("=")

    def __decrypt_ballot_id(self, encrypted_data: str) -> str:
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
        
    def __encrypt_vote(self, vote_data: str) -> str:
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(vote_data.encode())
        encrypted_data = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
        return encrypted_data

    def __decrypt_vote(self, encrypted_vote: str) -> str:
        encrypted_data = base64.b64decode(encrypted_vote)
        nonce = encrypted_data[:16] 
        tag = encrypted_data[16:32]  
        ciphertext = encrypted_data[32:]  

        cipher = AES.new(self._key, AES.MODE_EAX, nonce=nonce)
        decrypted_vote = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        return decrypted_vote
    
    def __encrypt_result(self, data: str) -> str:
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())

        encrypted_data = cipher.nonce + tag + ciphertext
        return base64.urlsafe_b64encode(encrypted_data).decode().rstrip("=")

    def __decrypt_result(self, encrypted_data: str) -> str:
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data + "==")

        nonce = encrypted_data_bytes[:16]
        tag = encrypted_data_bytes[16:32]
        ciphertext = encrypted_data_bytes[32:]

        cipher = AES.new(self._key, AES.MODE_EAX, nonce=nonce)

        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

        return decrypted_data.decode()

    def encrypt_ballot_id(self, data: str) -> str:
        return self.__encrypt_ballot_id(data)

    def decrypt_ballot_id(self, encrypted_data: str) -> str:
        return self.__decrypt_ballot_id(encrypted_data)
    
    def encrypt_vote(self, vote_data: str) -> str:
        return self.__encrypt_vote(vote_data)

    def decrypt_vote(self, encrypted_vote: str) -> str:
        return self.__decrypt_vote(encrypted_vote)
    
    def encrypt_result(self, data: str) -> str:
        return self.__encrypt_result(data)

    def decrypt_result(self, encrypted_data: str) -> str:
        return self.__decrypt_result(encrypted_data)
