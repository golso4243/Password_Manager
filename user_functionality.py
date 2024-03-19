import json, os, sys
from encryption import encrypt_password, decrypt_password
from hash import hash_password

# Function to register you.
def register(username, master_password):
    # Encrypt the master password before storing it
    hashed_master_password = hash_password(master_password)
    # Prepare user data for storage in dict
    user_data = {'username': username, 'master_password': hashed_master_password}
    
    # Define the path to the 'data' folder and the user data filename
    data_folder = 'data'
    file_name = 'user_data.json'
    user_data_file_path = os.path.join(data_folder, file_name)

    # Ensure the 'data' folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Check if file exists and is empty
    if os.path.exists(user_data_file_path) and os.path.getsize(user_data_file_path) == 0:
        # Open and write to file
        with open(user_data_file_path, 'w') as file:
            # Write user_data to dict in json format
            json.dump(user_data, file)
            # Registration Complete Message
            print("\n[+] Registration complete!!\n")
    # File does not exist, create a new one
    else:
        with open(user_data_file_path, 'w') as file:  # Changed from 'x' to 'w' to overwrite if necessary
            # Write user_data to dict in json format
            json.dump(user_data, file)
            # Registration Complete Message
            print("\n[+] Registration complete!!\n")


# Function to log you in.
def login(username, entered_password):
    try:
        # Read user_data.json 
        with open('data/user_data.json', 'r') as file:
            # Load json data from file into user_data dict
            user_data = json.load(file)
        # Retrieve stored password hash 
        stored_password_hash = user_data.get('master_password')
        # hash entered_password
        entered_password_hash = hash_password(entered_password)
        # Check password hashes match and username is correct
        if entered_password_hash == stored_password_hash and username == user_data.get('username'):
            # Successful login message
            print("\n[+] Login Successful..")
        # Failed Login
        else:
            print("\n[-] Invalid Login credentials. Please use the credentials you used to register.\n")
            sys.exit()
    # Not registered (exit)
    except Exception:
        print("\n[-] You have not registered. Please do that.\n")
        sys.exit()


# Function to view saved websites.
def view_websites():
    try:
        
        data_folder = 'data'
        file_name = 'passwords.json'
        password_file_path = os.path.join(data_folder, file_name)
        # Open Passwords file in read mode
        with open(password_file_path, 'r') as data:
            # Set view to parsed json data
            view = json.load(data)
            print("\n-----------------------------------------------")
            print("|               Saved Websites                |")
            print("-----------------------------------------------\n")
            # Interate through websites
            for x in view:
                print(x['website'])
            print('\n')
    # No passwords saved
    except FileNotFoundError:
        print("\n[-] You have not saved any passwords!\n")


# Function to add (save password).
def add_password(cipher, website, password):
    # Define the path to the 'data' folder and the passwords file
    data_folder = 'data'
    passwords_file = 'passwords.json'
    passwords_file_path = os.path.join(data_folder, passwords_file)

    # Ensure the 'data' folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Check if passwords.json exists
    if not os.path.exists(passwords_file_path):
        # If passwords.json doesn't exist, initialize it with an empty list
        data = []
    else:
        # Load existing data from passwords.json
        try:
            with open(passwords_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where passwords.json is empty or invalid JSON
            data = []
    
    # Encrypt the password using the provided cipher
    encrypted_password = encrypt_password(cipher, password)
    
    # Create a dictionary to store the website and password
    password_entry = {'website': website, 'password': encrypted_password}
    data.append(password_entry)
    
    # Save the updated list back to passwords.json in the 'data' folder
    with open(passwords_file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Function to retrieve a saved password.
def get_password(website, cipher):
    
    data_folder = 'data'
    passwords_file = 'passwords.json'
    passwords_file_path = os.path.join(data_folder, passwords_file)
    # Check if passwords.json exists
    if not os.path.exists(passwords_file_path):
        return None
    # Load existing data from passwords.json
    try:
        # Open in read mode and set to data
        with open(passwords_file_path, 'r') as file:
            data = json.load(file)
    # Error
    except json.JSONDecodeError:
        data = []
    # Loop through all the websites and check if the requested website exists.
    for entry in data:
        if entry['website'] == website:
            # Decrypt and return the password
            decrypted_password = decrypt_password(cipher, entry['password'])
            return decrypted_password
    return None
