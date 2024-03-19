import json, getpass, os, sys, pyperclip

from cryptography.fernet import Fernet
from encryption import generate_key, initialize_cipher, encrypt_password, decrypt_password
from hash import hash_password
from user_functionality import register, login, view_websites, add_password, get_password


# Define the path to the 'data' folder and the key filename
data_folder = 'data'
key_filename = 'encryption_key.key'
key_file_path = os.path.join(data_folder, key_filename)

# Ensure the 'data' folder exists
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Check for existing key file
if os.path.exists(key_file_path):
    # Read existing key
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
else:
    # Generate a new key
    key = generate_key()
    # Write key to key file within the 'data' folder
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)


# Initialize Cipher
cipher = initialize_cipher(key)


print("\n===============================================")
print("|           Python Password Manager           |")
print("===============================================\n")
# Infinite loop to keep the program running until the user chooses to quit.
while True:
    # Menu Options
    print("1. Register")
    print("2. Login")
    print("3. Quit\n")
    # User Input
    choice = input("Enter your choice >> ")
    # Register
    if choice == '1':  # If a user wants to register
        file = 'data/user_data.json'
        # Check if file exists and is not empty
        if os.path.exists(file) and os.path.getsize(file) != 0:
            # File exists (exit)
            print("\n[-] Master user already exists!!\n")
            continue
        # File/user doesn't exist
        else:
            # Input credentials
            print("\n----------------------------------------------")
            print("|           Enter Master Credentials         |")
            print("----------------------------------------------\n")
            username = input("Enter a Username: ")
            master_password = getpass.getpass("Enter a Master Password: ")
            # Register credentials
            register(username, master_password)
    # Login
    elif choice == '2':
        file = 'data/user_data.json'
        # File exists( user created)
        if os.path.exists(file):
            # Input credentials
            print("\n-----------------------------------------------")
            print("|                    Login                    |")
            print("-----------------------------------------------\n")
            username = input("Username: ")
            master_password = getpass.getpass("Master Password: ")
            # Login with credentials
            login(username, master_password)
        # User not registered
        else:
            print("\n[-] You have not registered. Please do that.\n")
            sys.exit()
        # Various options after a successful Login.
        while True:
            print("\n-----------------------------------------------")
            print("|                  Main Menu                  |")
            print("-----------------------------------------------\n")
            print("1. Add Password")
            print("2. Get Password")
            print("3. View Saved websites")
            print("4. Quit")
            password_choice = input("Enter your choice: ")
            # Add password
            if password_choice == '1':
                print("\n-----------------------------------------------")
                print("|                 Add Password                |")
                print("-----------------------------------------------\n")
                website = input("Enter website: ")
                password = getpass.getpass("Enter password: ")
                # Encrypt and add the password
                add_password(cipher, website, password)
                print("\n[+] Password added!\n")
            # Retrieve a password
            elif password_choice == '2':
                print("\n-----------------------------------------------")
                print("|              Retrieve Password              |")
                print("-----------------------------------------------\n")
                website = input("Enter website: ")
                decrypted_password = get_password(website, cipher)
                if website and decrypted_password:
                    # Copy password to clipboard for convenience
                    pyperclip.copy(decrypted_password)
                    print(f"\n[+] Password for {website}: {decrypted_password}\n[+] Password copied to clipboard.\n")
                # Password not found
                else:
                    print("\n[-] Password not found! Did you save the password?"
                        "\n[-] Use option 3 to see the websites you saved.\n")
            # View saved websites
            elif password_choice == '3':
                view_websites()
            # Quit
            elif password_choice == '4':  
                break
    # Quit        
    elif choice == '3': 
        break