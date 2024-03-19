from cryptography.fernet import Fernet

# Generate a secret key. (only run once)
def generate_key():
    return Fernet.generate_key()


# Initialize Fernet cipher with the provided key.
def initialize_cipher(key):
    return Fernet(key)


# Function to encrypt a  password.
def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode()).decode()


# Function to decrypt a  password.
def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()