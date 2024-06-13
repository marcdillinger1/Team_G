import json

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        with open(self.users_file, 'r') as file:
            users = json.load(file)
            return {user['email']: user for user in users}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(list(self.users.values()), file, indent=4)

    def register(self, email, password):
        if email in self.users:
            return None
        user_id = len(self.users) + 1
        self.users[email] = {'user_id': user_id, 'email': email, 'password': password, 'booking_history': []}
        self.save_users()
        return self.users[email]

    def login(self, email, password):
        user = self.users.get(email)
        if user and user['password'] == password:
            return user
        return None
