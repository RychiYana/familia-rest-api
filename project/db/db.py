import sqlite3


class DB_request:
    @staticmethod
    def check_user(email, password):
        query = f''' 
        select count(*) = 1
        FROM users u
        where u.email = '{email}' AND u.password = '{password}'
        '''
        return DB_request.request(query)[0][0] == 1
    
    def check_email(email):
        query = f''' 
        select count(*) = 1
        FROM users u
        where u.email = '{email}'
        '''
        return DB_request.request(query)[0][0] == 1
    
    @staticmethod
    def get_user(email, password):
        query = f''' 
        select u.id
        FROM users u
        where u.email = '{email}' AND u.password = '{password}'
        '''
        return DB_request.request(query)[0][0]
    
    @staticmethod
    def get_user_by_id(id):
        query = f'''
        select u.id, u.name, u.email 
        FROM users u
        where u.id = '{id}'
        '''
        print(query)
        return DB_request.request(query)
    
    @staticmethod
    def add_user(email, name, password):
        query = f''' 
        insert into users(email, name, password) values('{email}', '{name}', '{password}')
        '''
        DB_request.request(query, fetch=False)


    @staticmethod
    def request(query, fetch=True):
        result = None
        connection = sqlite3.connect('project/db/db.db')
        cursor = connection.cursor()
        cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result
    

