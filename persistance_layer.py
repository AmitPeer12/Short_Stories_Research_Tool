import sqlite3

# The DTO
class Stories:
    def __init__(self, id, story_name, author_id, word_count, word_stats):
        self.id = id
        self.story_name = story_name
        self.author_id = author_id
        self.word_count = word_count
        self.word_stats = word_stats

class Authors:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Generic DAO
class Dao:
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type
        self._table_name = dto_type.__name__.lower()

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        q_marks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, column_names, q_marks)

        self._conn.execute(stmt, params)

    def find(self, **key_values):
        column_names = key_values.keys()
        params = list(key_values.values())

        stmt = 'SELECT * FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, params)
        return self._dto_type(*c.fetchall()[0])

    # returns the first item in a table sorted by 'column'
    def find_first_by_order(self, column):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {} ORDER BY {} ASC LIMIT 1'.format(self._table_name, column))
        return self._dto_type(*c.fetchall()[0])

    def delete(self, **key_values):
        column_names = key_values.keys()
        params = list(key_values.values())

        stmt = 'DELETE FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, params)
    
    def update(self, column, value, id):
        self._conn.execute(
            'UPDATE {} SET {} = {} WHERE id = {}'.format(self._table_name, column, value, id))

# The Repository
class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.create_tables()
        self.stories = Dao(Stories, self._conn)
        self.authors = Dao(Authors, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS stories (
            id              INT         NOT NULL,
            story_name      TEXT        NOT NULL,
            author_id       TEXT        NOT NULL,
            word_count      INT         NOT NULL,
            word_stats      TEXT        NOT NULL,
            FOREIGN KEY(author_id)      REFERENCES authors(id)
        );
        
        CREATE TABLE IF NOT EXISTS authors (
            id              INT         PRIMARY KEY NOT NULL,
            name            TEXT        NOT NULL
        );
    """)


# the repository singleton
repo = _Repository()
