from src.movie import Movie
import sqlite3
import json

class DatabaseManager:

    def __init__(self, db_name='src/data/movies.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_movie_table()
        self.create_movie_category_table()
        
    def create_movie_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS movies (
                name TEXT PRIMARY KEY,
                description TEXT,
                director TEXT
            )
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def create_movie_category_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS movie_categories (
                movie_name TEXT,
                category_name TEXT,
                FOREIGN KEY (movie_name) REFERENCES movies(name),
                FOREIGN KEY (category_name) REFERENCES categories(name)
            )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def create_user_table(self, user:str):
        query = f'''
        CREATE TABLE IF NOT EXISTS "{user}" (
            name TEXT PRIMARY KEY,
            rating REAL,
            FOREIGN KEY (name) REFERENCES movies(name)
        )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def add_new_movie_to_db(self, movie: Movie):
        query_parameters = (movie.get_name(), movie.get_description(), movie.get_director())
        query = '''
            INSERT OR IGNORE INTO movies (name, description, director)
            VALUES (?, ?, ?)
        '''
        self.cursor.execute(query, query_parameters)
        self.connection.commit()

        for category in movie.get_categories():
            self.add_movie_category(movie.get_name(), category)



    def add_movie_category(self, movie_name: str, category_name: str):
        query = '''
            INSERT OR IGNORE INTO movie_categories (movie_name, category_name)
            VALUES (?, ?)
        '''
        self.cursor.execute(query, (movie_name, category_name))
        self.connection.commit()

    def add_movie_to_user_table(self, user:str, movie: Movie):
        self.add_new_movie_to_db(movie)
        self.create_user_table(user)
        query_parameters = (movie.get_name(), movie.get_rating())
        query = f'''
            INSERT OR IGNORE INTO {user} (name, rating)
            VALUES (?, ?)
            '''
        self.cursor.execute(query, query_parameters)
        self.connection.commit()

    def get_user_movies_names(self, user:str):
        query = f'SELECT name FROM {user}'
        self.cursor.execute(query)
        user_movies = self.cursor.fetchall()
        return [movie[0] for movie in user_movies]
    
    def get_movie_description(self, movie_name:str):
        query = '''
            SELECT description FROM movies WHERE name = ?
        '''
        self.cursor.execute(query, (movie_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_movie_director(self, movie_name:str):
        query = '''
            SELECT director FROM movies WHERE name = ?
        '''
        self.cursor.execute(query, (movie_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_user_movies_ratings(self, user:str, movie_name:str):
        query = f'''
            SELECT rating FROM {user} WHERE name = ?
        '''
        self.cursor.execute(query, (movie_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_movie_categories(self, movie_name:str):
        query = '''
            SELECT category_name FROM movie_categories WHERE movie_name = ?
        '''
        self.cursor.execute(query, (movie_name,))
        categories = self.cursor.fetchall()
        return [category[0] for category in categories]

    def get_all_user_table_movies(self,user:str):
        movies = []
        movie_names = self.get_user_movies_names(user)
        for movie_name in movie_names:
            rating = self.get_user_movies_ratings(user, movie_name)
            description = self.get_movie_description(movie_name)
            director = self.get_movie_director(movie_name)
            categories = self.get_movie_categories(movie_name)
            movies.append(Movie(movie_name, description, categories, rating, director))
        return movies
    
    def update_movie_rating(self, user:str, movie_name:str, new_rating: float):
        
        query_parameters = (movie_name,new_rating,movie_name)
        query = f'''
            UPDATE {user} 
            SET name = ?, rating = ?
            WHERE name = ?
        '''
        self.cursor.execute(query, query_parameters )
        self.connection.commit()

    def get_user_movie_info(self, user:str, movie_name:str):
        rating = self.get_user_movies_ratings(user, movie_name)
        description = self.get_movie_description(movie_name)
        director = self.get_movie_director(movie_name)
        categories = self.get_movie_categories(movie_name)
        return Movie(movie_name, description, categories, rating, director)
        


    def close(self):
        self.connection.close()



