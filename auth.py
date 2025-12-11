import bcrypt

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_default_users():
    """Create default users for testing"""
    from db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    # Default users
    users = [
        ("admin", "admin123", "admin"),
        ("cyber", "cyber123", "cybersecurity"),
        ("it", "it123", "it_operations")
    ]
    
    for username, password, role in users:
        db.register_user(username, password, role)
    
    print("Default users created")
    
    # Close database
    db.close()

if __name__ == "__main__":
    create_default_users()
    print("Run 'python db_manager.py' first to create database")
    
def initialize_database():
    """Initialize the database with tables and data"""
    from db_manager import DatabaseManager
    
    print("=== Setting up database ===")
    
    # Create database manager 
    db = DatabaseManager()
    
    # Load users from users.txt
    print("Loading users from users.txt...")
    db.migrate_users()
    
    # Load CSV data
    print("Loading CSV data...")
    db.load_csv_data()
    
    # Add your default users too
    users = [
        ("admin", "admin123", "admin"),
        ("cyber", "cyber123", "cybersecurity"),
        ("it", "it123", "it_operations")
    ]
    
    for username, password, role in users:
        db.register_user(username, password, role)
    
    db.close()
    print("=== Database setup complete! ===")
    print("\nYou can now login with:")
    print("- jordan / password123 (admin)")
    print("- admin / admin123 (admin)")
    print("- cyber / cyber123 (cybersecurity)")
    print("- it / it123 (it_operations)")
    print("- data / password123 (data_science)")

# Update the __main__ block in YOUR auth.py:
if __name__ == "__main__":
    # Remove or comment out your current create_default_users() call
    # create_default_users()  # COMMENT THIS OUT
    # print("Run 'python db_manager.py' first to create database")  # COMMENT THIS OUT
    
    # ADD THIS INSTEAD:
    initialize_database()    