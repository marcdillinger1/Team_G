import json

class UserManager: # Initialize UserManager with a file path for user data.
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):  # Load user data from JSON, indexing it by email for quick lookup.
        with open(self.users_file, 'r') as file:
            users = json.load(file)
            return {user['email']: user for user in users}

    def save_users(self): # Save the current state of user data back to the JSON file.
        with open(self.users_file, 'w') as file:
            json.dump(list(self.users.values()), file, indent=4)

    def register(self, email, password):  # Register a new user with an email and password.
        if email in self.users:
            return None
        user_id = len(self.users) + 1
        self.users[email] = {'user_id': user_id, 'email': email, 'password': password, 'booking_history': []}
        self.save_users()
        return self.users[email]

    def login(self, email, password):  # Attempt to log in a user with their email and password.
        user = self.users.get(email)
        if user and user['password'] == password:
            return user
        return None
