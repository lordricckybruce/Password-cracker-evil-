#!/bin/python3

import hashlib
import itertools
import string
import multiprocessing

# Function to hash a password with the specified hash type
def hash_password(password, hash_type):
    if hash_type == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif hash_type == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash type")

# Brute-force password cracker function
def crack_password_segment(start, end, chars, hash_value, hash_type):
    for length in range(1, 9):  # Iterate from 1 to max length of 8
        for password in itertools.product(chars, repeat=length):
            password_str = "".join(password)
            if hash_password(password_str, hash_type) == hash_value:
                return password_str
    return None

# Function to crack password using multiprocessing
def crack_password(hash_value, hash_type):
    chars = string.ascii_letters + string.digits + string.punctuation  # Expanded character set
    pool_size = multiprocessing.cpu_count()  # Use multiple CPU cores

    # Split the task into segments for parallel processing
    pool = multiprocessing.Pool(pool_size)
    result = pool.starmap(crack_password_segment, [(start, end, chars, hash_value, hash_type) for start, end in zip(range(0, pool_size), range(1, pool_size + 1))])

    # Collect the result
    for res in result:
        if res:
            return res
    return None

# Example usage
hash_value = "5f4dcc3b5aa765d61d8327deb882cf99"  # Hash value of the password (example: 'password' in MD5)
hash_type = "md5"  # Hash type used for the password

password = crack_password(hash_value, hash_type)
if password:
    print(f"Password found: {password}")
else:
    print("Password not found")

