import sqlite3
import pandas as pd
import bcrypt

class DatabaseManager:
    def __init__(self, db_name="multi_domain.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create tables for users and domains"""
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        # Cybersecurity incidents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                date TEXT,
                severity TEXT,
                category TEXT,
                status TEXT,
                resolution_time_hours INTEGER
            )
        ''')
        
        # IT Tickets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                created_date TEXT,
                priority TEXT,
                status TEXT,
                assigned_to TEXT,
                category TEXT,
                resolution_time_hours INTEGER
            )
        ''')
        
        self.conn.commit()
    
    def migrate_users(self):
        """Migrate users from text file to database"""
        try:
            with open('users.txt', 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        username, password_hash, role = parts[:3]
                        try:
                            self.cursor.execute(
                                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                (username, password_hash, role)
                            )
                        except:
                            pass  # User already exists
            
            self.conn.commit()
            print("Users migrated to database")
        except:
            print("No users.txt file found")
    
    def load_csv_data(self):
        """Load CSV data into database"""
        # Load cybersecurity data
        try:
            cyber_df = pd.read_csv('DATA/cyber_incidents.csv')
            cyber_df.to_sql('cyber_incidents', self.conn, if_exists='replace', index=False)
            print(f"Loaded {len(cyber_df)} cyber incidents")
        except:
            print("Could not load cyber_incidents.csv")
        
        # Load IT tickets data
        try:
            it_df = pd.read_csv('DATA/it_tickets.csv')
            it_df.to_sql('it_tickets', self.conn, if_exists='replace', index=False)
            print(f"Loaded {len(it_df)} IT tickets")
        except:
            print("Could not load it_tickets.csv")
    
    def register_user(self, username, password, role="user"):
        """Register a new user with bcrypt hashing"""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash.decode('utf-8'), role)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def verify_user(self, username, password):
        """Verify user login credentials"""
        self.cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        
        if result:
            stored_hash = result[0].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False
    
    def get_user_role(self, username):
        """Get user's role"""
        self.cursor.execute(
            "SELECT role FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_cyber_incidents(self):
        """Get all cybersecurity incidents"""
        return pd.read_sql("SELECT * FROM cyber_incidents", self.conn)
    
    def get_it_tickets(self):
        """Get all IT tickets"""
        return pd.read_sql("SELECT * FROM it_tickets", self.conn)
    
    def close(self):
        """Close database connection"""
        self.conn.close()