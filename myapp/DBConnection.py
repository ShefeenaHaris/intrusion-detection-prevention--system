# import mysql.connector
#
# class Db:
#
#     def __init__(self):
#
#         self.cnx = mysql.connector.connect(host="localhost", user="root", password="123456789", database="intrusions")
#         self.cur = self.cnx.cursor(dictionary=True)
#
#
#     def select(self, q):
#         self.cur.execute(q)
#         return self.cur.fetchall()
#
#     def selectOne(self, q):
#         self.cur.execute(q)
#         return self.cur.fetchone()
#
#
#     def insert(self, q):
#
#         print(q)
#         self.cur.execute(q)
#         self.cnx.commit()
#         return self.cur.lastrowid
#
#     def update(self, q):
#         self.cur.execute(q)
#         self.cnx.commit()
#         return self.cur.rowcount
#
#     def delete(self, q):
#         self.cur.execute(q)
#         self.cnx.commit()
#         return self.cur.rowcount
#
# import mysql.connector
# from mysql.connector import Error
#
# class Db:
#     def __init__(self):
#         """✅ FIXED: No more caching_sha2_password errors"""
#
#         self.cnx = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="123456789",
#             database="intrusions",
#             auth_plugin='mysql_native_password',  # ✅ FIXES auth error
#             autocommit=True
#         )
#         self.cur = self.cnx.cursor(dictionary=True)
#         print("✅ Database connected successfully")
#
#
#     def insert_log(self, ipaddress, log_type, customer_id='4'):
#         """✅ NEW: Perfect for intrusion logs - default customer_id=1"""
#
#         query = """INSERT INTO `myapp_logs` (`date`,`time`,`ipaddress`,`log`,`CUSTOMER_id`) VALUES (CURDATE(), CURTIME(), %s, %s, %s)"""
#         self.cur.execute(query, (ipaddress, log_type, customer_id))
#         print(f"✅ Logged {log_type}: {ipaddress}")
#         return self.cur.lastrowid
#
#
#     def insert(self, q):
#         """✅ SAFE raw insert - bypasses foreign key issues"""
#         try:
#             self.cur.execute("SET SESSION FOREIGN_KEY_CHECKS = 0")
#             self.cur.execute(q)
#             self.cur.execute("SET SESSION FOREIGN_KEY_CHECKS = 1")
#             return self.cur.lastrowid
#         except Error as e:
#             print(f"❌ Insert error: {e}")
#             return None
#
#     def select(self, q):
#         try:
#             self.cur.execute(q)
#             return self.cur.fetchall()
#         except Error as e:
#             print(f"❌ Select error: {e}")
#             return []
#
#     def close(self):
#         if self.cur:
#             self.cur.close()
#         if self.cnx and self.cnx.is_connected():
#             self.cnx.close()
#             print("✅ Database closed")

import mysql.connector
from mysql.connector import Error


class Db:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="intrusions",
            auth_plugin='mysql_native_password',
            autocommit=True
        )
        self.cur = self.cnx.cursor(dictionary=True)
        print("✅ Database connected successfully")

    def insert_log(self, ipaddress, log_type, customer_id='4'):
        """Insert intrusion log — default customer_id=4"""
        query = """
            INSERT INTO `myapp_logss` (`date`, `time`, `ipaddress`, `log`, `CUSTOMER_id`)
            VALUES (CURDATE(), CURTIME(), %s, %s, %s)
        """
        try:
            self.cur.execute(query, (ipaddress, log_type, customer_id))
            print(f"✅ Logged {log_type}: {ipaddress}")
            return self.cur.lastrowid
        except Error as e:
            print(f"❌ insert_log error: {e}")
            return None

    def insert(self, q):
        """Raw insert — use only when necessary"""
        try:
            self.cur.execute("SET SESSION FOREIGN_KEY_CHECKS = 0")
            self.cur.execute(q)
            self.cur.execute("SET SESSION FOREIGN_KEY_CHECKS = 1")
            return self.cur.lastrowid
        except Error as e:
            print(f"❌ Insert error: {e}")
            return None

    def select(self, q):
        try:
            self.cur.execute(q)
            return self.cur.fetchall()
        except Error as e:
            print(f"❌ Select error: {e}")
            return []

    def close(self):
        if self.cur:
            self.cur.close()
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            print("✅ Database closed")