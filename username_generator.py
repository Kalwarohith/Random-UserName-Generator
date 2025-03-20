import random
import json
import os

# Default word lists
adjectives = ["Cool", "Happy", "Fast", "Brave", "Clever", "Witty", "Lucky", "Mighty", "Silly", "Fierce"]
nouns = ["Tiger", "Dragon", "Falcon", "Panda", "Wizard", "Knight", "Phoenix", "Shadow", "Ninja", "Jester"]

# File to store generated usernames
FILENAME = "usernames.json"

def load_existing_usernames():
    """Load existing usernames from a JSON file."""
    if not os.path.exists(FILENAME):
        return set()
    try:
        with open(FILENAME, "r") as file:
            return set(json.load(file))
    except (json.JSONDecodeError, FileNotFoundError):
        return set()

def save_to_file(usernames):
    """Saves unique usernames to a JSON file."""
    existing_usernames = load_existing_usernames()
    new_usernames = [u for u in usernames if u not in existing_usernames]
    if new_usernames:
        with open(FILENAME, "w") as file:
            json.dump(list(existing_usernames | set(new_usernames)), file, indent=4)
        print(f"{len(new_usernames)} usernames saved to '{FILENAME}'!")
    else:
        print("All generated usernames already exist in the file. No new names were saved.")

def generate_username(add_numbers=True, add_special_chars=False, length=None, pattern="AdjectiveNoun"):
    """Generates a random username based on user preferences."""
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    username = noun + adj if pattern == "NounAdjective" else adj + noun
    if add_numbers:
        username += str(random.randint(10, 99))
    if add_special_chars:
        username += random.choice("!@#$%^&*")
    return username[:length] if length else username

def add_custom_words():
    """Allows the user to add custom words to the adjective and noun lists."""
    global adjectives, nouns
    custom_adj = input("Enter new adjectives (comma-separated) or press Enter to skip: ").strip()
    custom_nouns = input("Enter new nouns (comma-separated) or press Enter to skip: ").strip()
    if custom_adj:
        adjectives.extend(word.strip().capitalize() for word in custom_adj.split(","))
    if custom_nouns:
        nouns.extend(word.strip().capitalize() for word in custom_nouns.split(","))
    print("Custom words added successfully!\n")

def main():
    """Interactive menu-driven username generator."""
    existing_usernames = load_existing_usernames()
    print("Welcome to the Advanced Random Username Generator!")
    while True:
        print("\n--- MENU ---")
        print("1. Generate Username(s)")
        print("2. Add Custom Words")
        print("3. Show Previously Generated Usernames")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            try:
                count = int(input("How many usernames do you want to generate? (1-10): ").strip())
                if not (1 <= count <= 10):
                    print("Please enter a number between 1 and 10.")
                    continue
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue
            add_numbers = input("Include numbers? (yes/no): ").strip().lower() == "yes"
            add_special_chars = input("Include special characters? (yes/no): ").strip().lower() == "yes"
            length = input("Set a maximum username length (press Enter to skip): ").strip()
            length = int(length) if length.isdigit() else None
            pattern = input("Choose format (AdjectiveNoun/NounAdjective): ").strip()
            pattern = pattern if pattern in ["AdjectiveNoun", "NounAdjective"] else "AdjectiveNoun"
            generated_usernames = set()
            while len(generated_usernames) < count:
                username = generate_username(add_numbers, add_special_chars, length, pattern)
                if username not in existing_usernames:
                    generated_usernames.add(username)
                    existing_usernames.add(username)
            print("\nGenerated Usernames:")
            for username in generated_usernames:
                print(f" - {username}")
            save_to_file(generated_usernames)
        elif choice == "2":
            add_custom_words()
        elif choice == "3":
            print("\nPreviously Generated Usernames:")
            if existing_usernames:
                for username in existing_usernames:
                    print(f" - {username}")
            else:
                print("No usernames found.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
