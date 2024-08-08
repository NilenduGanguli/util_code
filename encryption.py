from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    # Generate a key based on the password using SHA-256
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).digest()
    return base64.urlsafe_b64encode(hashed_password)

def encrypt(text: str, password: str) -> str:
    key = generate_key(password)
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode('utf-8'))
    return encrypted_text.decode('utf-8')

def decrypt(encrypted_text: str, password: str) -> str:
    key = generate_key(password)
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text.encode('utf-8'))
    return decrypted_text.decode('utf-8')

# Example usage
if __name__ == "__main__":
    original_text = "This is a secret message."
    password = "mypassword"

    # Encrypt the text
    encrypted = encrypt(original_text, password)
    print(f"Encrypted: {encrypted}")

    # Decrypt the text
    decrypted = decrypt(encrypted, password)
    print(f"Decrypted: {decrypted}")
