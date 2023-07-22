import sqlite3

class CRUDSQLite:
    # DB_FILE = "DataSet/DataSet/STORE_db.DB"
    DB_FILE = "BDStore/DataSet/DataSet/STORE_db.DB"
    def __init__(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        

    def get_user_by_id(self, id):
        query = '''
            SELECT * FROM customers_dataset WHERE customer_id == ?
        '''
        cursor = self.conn.execute(query, (id,))
        return cursor.fetchone()

    def get_all_customers(self):
        query = '''
            SELECT * FROM customers_dataset
        '''
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    
    db = CRUDSQLite()


    # Consulta de um registro pelo ID
    result = db.get_user_by_id("06b8999e2fba1a1fbc88172c00ba8bc7")
    if result:
        print("Registro encontrado:")
        print(result)
    else:
        print("Registro não encontrado.")



    db.close_connection()
