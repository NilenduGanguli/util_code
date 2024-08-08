def xor_encrypt_decrypt(text: str, password: str) -> str:
    # Repeat the password so that its length matches the text length
    repeated_password = (password * (len(text) // len(password) + 1))[:len(text)]
    # Perform XOR between each character in the text and the corresponding character in the password
    encrypted_decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, repeated_password))
    return encrypted_decrypted

def encrypt(text: str, password: str) -> str:
    return xor_encrypt_decrypt(text, password)

def decrypt(encrypted_text: str, password: str) -> str:
    return xor_encrypt_decrypt(encrypted_text, password)

# Example usage
if __name__ == "__main__":
    original_text = "SecretMessage123"
    password = "mypassword"

    # Encrypt the text
    encrypted = encrypt(original_text, password)
    print(f"Encrypted: {encrypted}")

    # Decrypt the text
    decrypted = decrypt(encrypted, password)
    print(f"Decrypted: {decrypted}")
