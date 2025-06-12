from movie import Movie
import sqlite3
import os

class DatabaseManager:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'data/movies.db')
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                name TEXT PRIMARY KEY,
                description TEXT,
                director TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movie_categories (
                movie_name TEXT,
                category_name TEXT,
                FOREIGN KEY (movie_name) REFERENCES movies(name)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                movie_name TEXT PRIMARY KEY,
                rating REAL,
                FOREIGN KEY (movie_name) REFERENCES movies(name)
            )
        ''')

        self.connection.commit()

    def add_movie(self, movie: Movie):
        self.cursor.execute('''
            INSERT OR IGNORE INTO movies (name, description, director)
            VALUES (?, ?, ?)
        ''', (movie.get_name(), movie.get_description(), movie.get_director()))

        for category in movie.get_categories():
            self.cursor.execute('''
                INSERT OR IGNORE INTO movie_categories (movie_name, category_name)
                VALUES (?, ?)
            ''', (movie.get_name(), category))

        self.cursor.execute('''
            INSERT OR REPLACE INTO ratings (movie_name, rating)
            VALUES (?, ?)
        ''', (movie.get_name(), movie.get_rating()))

        self.connection.commit()

    def get_all_movies_with_ratings(self):
        self.cursor.execute('''
            SELECT m.name, m.description, m.director, r.rating
            FROM movies m
            JOIN ratings r ON m.name = r.movie_name
        ''')
        rows = self.cursor.fetchall()
        movies = []
        for row in rows:
            name, description, director, rating = row
            self.cursor.execute('SELECT category_name FROM movie_categories WHERE movie_name = ?', (name,))
            categories = [r[0] for r in self.cursor.fetchall()]
            movies.append(Movie(name, description, categories, rating, director))
        return movies

    def get_last_movies_with_average(self, limit=5):
        self.cursor.execute('''
            SELECT m.name, m.description, m.director, r.rating
            FROM ratings r
            JOIN movies m ON m.name = r.movie_name
            ORDER BY rowid DESC
            LIMIT ?
        ''', (limit,))
        rows = self.cursor.fetchall()
        filmes = []
        soma = 0
        for row in rows:
            name, description, director, rating = row
            self.cursor.execute('SELECT category_name FROM movie_categories WHERE movie_name = ?', (name,))
            categories = [r[0] for r in self.cursor.fetchall()]
            filmes.append({
                'title': name,
                'description': description,
                'director': director,
                'categories': categories,
                'rating': rating
            })
            soma += rating
        media = soma / len(filmes) if filmes else 0
        return media, filmes

    def get_top_categories(self, limit=5):
        self.cursor.execute('''
            SELECT category_name, COUNT(*) as total
            FROM movie_categories
            GROUP BY category_name
            ORDER BY total DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
