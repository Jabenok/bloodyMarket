import mysql.connector
from flask import current_app

class Database:
    def __init__(self):
        self.encryption_key = 'key'
    
    def get_connection(self):
        """Создание подключения к базе данных"""
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='bloodymarket'
        )
        return connection
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Универсальный метод выполнения запросов"""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            connection.commit()
            return result
            
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
    
    # Специфические методы для работы с пользователями
    def get_user_by_credentials(self, username, password):
        """Поиск пользователя по логину и паролю"""
        query = """
            SELECT id, name
            FROM user
            WHERE name = %s AND password = AES_ENCRYPT(%s, %s)
        """
        return self.execute_query(query, (username, password, self.encryption_key), fetch_one=True)
    
    def get_user_by_username(self, username):
        """Проверка существования пользователя"""
        query = "SELECT id FROM user WHERE name = %s"
        return self.execute_query(query, (username,), fetch_one=True)
    
    def create_user(self, username, password):
        """Создание нового пользователя"""
        query = """
            INSERT INTO user (name, password)
            VALUES (%s, AES_ENCRYPT(%s, %s))
        """
        return self.execute_query(query, (username, password, self.encryption_key))
    
    def get_user_by_id(self, user_id):
        """Получение пользователя по ID"""
        query = "SELECT id, name FROM user WHERE id = %s"
        return self.execute_query(query, (user_id,), fetch_one=True)

# Создаем экземпляр для использования
db = Database()