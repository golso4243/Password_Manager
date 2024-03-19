import hashlib

# Master Password Hashing Function
def hash_password(password):
    # Initialize new SHA-256 hash object
    sha256 = hashlib.sha256()
    # Convert password to bytes and Update hash object
    sha256.update(password.encode())
    # Return hexidecimal digest of hash object
    return sha256.hexdigest()