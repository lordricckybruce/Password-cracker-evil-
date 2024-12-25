#!/bin/python3
import re
import hashlib
import requests

# Function to check password strength
def check_password_strength(password):
    # Criteria for password strength
    length_criteria = len(password) >= 8
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    number_criteria = re.search(r'[0-9]', password) is not None
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    # Common weak passwords list
    weak_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123']

    # Check if the password is in the weak passwords list
    if password in weak_passwords:
        return "Weak password - commonly used password."

    # Determine overall strength
    if length_criteria and lowercase_criteria and uppercase_criteria and number_criteria and special_char_criteria:
        return "Strong password!"
    elif length_criteria and (lowercase_criteria or uppercase_criteria) and number_criteria:
        return "Moderate password."
    else:
        return "Weak password."

# Function to check if the password is exposed in any data breach
def check_password_breach(password):
    # Convert the password into its SHA1 hash (uppercase)
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()

    # Send only the first 5 characters of the hash (prefix) to the API
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Send request to the Have I Been Pwned API
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    # If the API request is successful
    if response.status_code == 200:
        hashes = response.text.splitlines()
        
        # Iterate through the returned hashes and check if the suffix matches
        for hash_entry in hashes:
            hash_suffix, count = hash_entry.split(':')
            if hash_suffix == suffix:
                return f"Password has been exposed {count} times in data breaches."
        
        return "Password is not found in any known breaches."
    else:
        return "Error checking password breach status."

# Main function to check both password strength and breach status
def analyze_password(password):
    # Check password strength
    strength = check_password_strength(password)
    
    # Check if the password is in known data breaches
    breach_status = check_password_breach(password)
    
    # Return both results
    return strength, breach_status

# Example Usage
if __name__ == "__main__":
    password = input("Enter a password to analyze: ")
    strength, breach_status = analyze_password(password)
    
    print(f"Password Strength: {strength}")
    print(f"Breach Status: {breach_status}")


