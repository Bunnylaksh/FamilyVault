import sqlite3
from datetime import datetime

class DatabaseService:
    
    def __init__(self):
        self.connection=sqlite3.connect("vault.db")
        self.cursor=self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT NOT NULL,
            account_number TEXT,
            IFSC_code TEXT,
            MICR_code TEXT,
            created_date TEXT,
            updated_date TEXT
            )"""
            )
            
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_details(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_id INTEGER NOT NULL,
            use_type TEXT NOT NULL,
            User_name TEXT NOT NULL,
            User_Password Text,
            User_Pin TEXT,
            created_date TEXT,
            updated_date TEXT,            
            FOREIGN KEY(acc_id) REFERENCES accounts(id)
            )"""
            )
            
        self.connection.commit()     
        
        
        
        
    def add_account(self,bank_name, account_number, IFSC_code, MICR_code):
        now =datetime.now().isoformat()
        
        self.cursor.execute("""
        INSERT INTO accounts(
            bank_name, 
            account_number, 
            IFSC_code, 
            MICR_code,
            created_date,
            updated_date
            )
            VALUES(?,?,?,?,?,?)""",(bank_name, account_number, IFSC_code, MICR_code, now, now))
        self.connection.commit()         
        
        
    def add_account_details(self,acc_id, use_type, User_name, User_Password, User_Pin):
        now =datetime.now().isoformat()
        self.cursor.execute("""
        INSERT INTO account_details(
            acc_id, 
            use_type, 
            User_name, 
            User_Password,
            User_Pin,
            created_date,
            updated_date            
            )
            VALUES(?,?,?,?,?,?,?)""",(acc_id, use_type, User_name, User_Password, User_Pin, now, now))
        self.connection.commit()   
      
        
    def get_account(self):
        self.cursor.execute("""
        SELECT
            id,
            bank_name,
            account_number,
            IFSC_code,
            MICR_code
            created_date
        FROM accounts
        ORDER BY id
        """)
        
        return self.cursor.fetchall()
        
    def get_account_by_id(self,account_id):
        self.cursor.execute("""
        SELECT
            id,
            bank_name,
            account_number,
            IFSC_code,
            MICR_code
            created_date,
            updated_date
        FROM accounts
        where id=?
        """,(account_id,))
        
        return self.cursor.fetchone()        
        
    def get_account_details_by_id(self, account_id):
        self.cursor.execute("""
        SELECT
            a1.id,
            a2.bank_name,
            a2.account_number,
            a1.use_type,
            a1.User_name,
            a1.User_Password,
            a1.User_Pin,
            a1.created_date,
            a1.updated_date
        FROM account_details a1
        INNER JOIN accounts a2 ON a2.id=a1.acc_id
        WHERE a1.acc_id=?
        """,(account_id,))
        
        return self.cursor.fetchall() 
        
    def get_account_line_details_by_id(self, acc_id, line_id):
        self.cursor.execute("""
        SELECT
            a1.id,
            a1.use_type,
            a1.User_name,
            a1.User_Password,
            a1.User_Pin,
            a1.created_date,
            a1.updated_date
        FROM account_details a1
        WHERE a1.acc_id=? and a1.id=?
        """,(acc_id,line_id))
        
        return self.cursor.fetchall()   

    def update_acc_line_details(self, acc_line_id, field_name, value_name):
        now =datetime.now().isoformat()
        for i in range(len(field_name)):
            query=f"""update account_details 
                set {field_name[i]}=?
            WHERE id=?"""
            self.cursor.execute(query,(value_name[i],acc_line_id,))
            self.cursor.execute("""update account_details set updated_date=? WHERE id =?""",(now,acc_line_id,))
            self.connection.commit()
        
    def delete_account_by_id(self, account_detail_id):
        self.cursor.execute("""
        DELETE FROM account_details WHERE id=?""",(account_detail_id,))
        self.connection.commit()