import pyodbc #type: ignore


server = 'localhost,1433'
database = 'hermesMedica'
username = 'sa'
password = '1q2w3e4r*'

CONN_STR = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

class Database:
    def __init__(self):
        self.conn = pyodbc.connect(CONN_STR, autocommit=True)
        self.cursor = self.conn.cursor()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        if row is None:
            return None
        columns = [column[0].lower() for column in self.cursor.description]
        return dict(zip(columns, row))

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        columns = [column[0].lower() for column in self.cursor.description]
        results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return results

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
    def executeAndReturnId(self, query, params=()):
        if query.strip().upper().startswith("INSERT"):
            full_query = f"{query}; SELECT SCOPE_IDENTITY();"
            self.cursor.execute(full_query, params)

            while self.cursor.nextset():
                try:
                    result = self.cursor.fetchone()
                    if result:
                        inserted_id = result[0]
                        return inserted_id
                except:
                    pass
            return None
        else:
            self.cursor.execute(query, params)
            return None
    def close(self):
        self.cursor.close()
        self.conn.close()
