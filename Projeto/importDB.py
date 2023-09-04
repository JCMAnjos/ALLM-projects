import sqlite3
import json

class CRUDSQLite:
    # DB_FILE = "DataSet/DataSet/STORE_db.DB"
    DB_FILE = "/content/STORE_db.DB"
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
            SELECT customer_id FROM customers_dataset
        '''
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def get_all_customers_jsonFormat(self):
        # query = '''
        #     SELECT customer_id FROM customers_dataset
        # '''

        query = '''
                SELECT

                        json_object(
                            'customer_id', customer_id
                            )

                FROM customers_dataset

        '''
        cursor = self.conn.execute(query)
        result = cursor.fetchall()

        if result:
            res = []
            if(len(result)>1):
                for item in result:
                    res.append(json.loads(item[0]))
            else:
                res.append(json.loads(result[0]))
            return res

        return result

    def get_order_by_id(self, id):
        query = '''
            SELECT * FROM orders_dataset WHERE order_id == ?
        '''
        cursor = self.conn.execute(query, (id,))
        return cursor.fetchone()

    def get_order_by_user_id(self, id):
        query = '''
            SELECT * FROM orders_dataset WHERE customer_id == ?;
        '''

        cursor = self.conn.execute(query, (id,))
        return cursor.fetchone()

    def get_order_by_user_id_jsonFormat(self, id):

        query = '''
                SELECT

                        json_object(
                            'order_id', order_id,
                            'customer_id', customer_id,
                            'order_status', order_status,
                            'order_purchase_timestamp', order_purchase_timestamp,
                            'order_approved_at', order_approved_at,
                            'order_delivered_carrier_date', order_delivered_carrier_date,
                            'order_delivered_customer_date', order_delivered_customer_date,
                            'order_estimated_delivery_date', order_estimated_delivery_date
                            )

                FROM orders_dataset WHERE customer_id == ?

        '''
        cursor = self.conn.execute(query, (id,))
        result = cursor.fetchone()

        if result:
            res = []
            if(len(result)>1):
                for item in result:
                    res.append(json.loads(item[0]))
            else:
                res.append(json.loads(result[0]))

            return res

        return result



    def get_orderItems_by_id(self, id):
        query = '''
            SELECT * FROM orders_items_dataset WHERE order_id == ?
        '''
        cursor = self.conn.execute(query, (id,))
        return cursor.fetchone()

    def get_product_by_id(self, id):
        query = '''
            SELECT * FROM products_dataset WHERE product_id == ?
        '''
        cursor = self.conn.execute(query, (id,))
        return cursor.fetchone()


    def close_connection(self):
        self.conn.close()