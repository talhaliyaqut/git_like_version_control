import hashlib
import json
import os

class FileSHA256Manager:
    def __init__(self, file_path, db_path="sha_dictionary.json"):
        self.file_path = file_path
        self.db_path = db_path
        self.sha_dictionary = self.load_sha_dictionary()

    def generate_and_update_sha256_hash(self):
        """Generate a SHA-256 hash for the file and update the dictionary if the hash is not already present."""
        sha256_hash = hashlib.sha256()
        try:
            with open(self.file_path, "rb") as file:
                while chunk := file.read(8192):
                    sha256_hash.update(chunk)
            hash_value = sha256_hash.hexdigest()

            if hash_value not in self.sha_dictionary:
                with open(self.file_path, "r") as file:
                    self.sha_dictionary[hash_value] = file.read()
                self.save_sha_dictionary()  # Save the updated dictionary to the JSON file

            return hash_value
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' was not found.")
            return None

    def load_sha_dictionary(self):
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            return {}  # Return an empty dictionary if the file doesn't exist or is empty
        """Load the SHA dictionary from a JSON file."""
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as file:
                return json.load(file)

    def save_sha_dictionary(self):
        """Save the SHA dictionary to a JSON file."""
        with open(self.db_path, "w") as file:
            json.dump(self.sha_dictionary, file, indent=4)

# Example usage
file_path = "example.txt"  # Replace with your file path

manager = FileSHA256Manager(file_path)
hash_value = manager.generate_and_update_sha256_hash()
if hash_value:
    print(f"The SHA-256 hash of the file content is: {hash_value}")
