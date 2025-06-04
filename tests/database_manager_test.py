from src.database_manager import DatabaseManager
from src.movie import Movie
import pytest 
import json
import os

@pytest.fixture
def db_manager():
    db_path = ':memory:'
    db_manager = DatabaseManager(db_path)
    db_manager.create_user_table('test_user')  # Create a user table for testing
    yield db_manager
    db_manager.close()
    

@pytest.fixture
def movie_sample_1():
    name = 'Movie 1 test name'
    description = 'This is a test movie with no categories assigned'
    categories = ['Test Category One']
    rating = 2.5
    director = 'Test author'

    return Movie(name, description, categories, rating, director)

@pytest.fixture
def movie_sample_2():
    name = 'Movie 2 test name'
    description = 'This is a test movie with one category assigned'
    categories = ['Test Category One','Test Category Two']
    rating = 3.5
    director = 'Test author'

    return Movie(name, description, categories, rating, director)

class TestDatabaseManager:
    
    def test_user_create_table(self, db_manager):
        
        
        db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_user'")
        result = db_manager.cursor.fetchone()
        
        assert result is not None
        assert result[0] == 'test_user' 

    def test_add_movie_to_user_table(self, db_manager, movie_sample_1):
        
        db_manager.add_movie_to_user_table('test_user', movie_sample_1)
        
        db_manager.cursor.execute("SELECT * FROM test_user WHERE name=?", (movie_sample_1.get_name(),))
        result = db_manager.cursor.fetchone()
        
        
        assert result[0] == movie_sample_1.get_name()
        assert result[1] == movie_sample_1.get_rating()
    

    def test_get_all_user_table_movies(self, db_manager, movie_sample_1, movie_sample_2):
        
        db_manager.add_movie_to_user_table('test_user', movie_sample_1)
        db_manager.add_movie_to_user_table('test_user', movie_sample_2)
        
        movies = db_manager.get_all_user_table_movies('test_user')
        
        assert len(movies) == 2
        assert movies[0].get_name() == movie_sample_1.get_name()
        assert movies[1].get_name() == movie_sample_2.get_name()
    
    def test_update_movie_rating_in_user_table(self, db_manager, movie_sample_1):
        
        db_manager.add_movie_to_user_table('test_user', movie_sample_1)
        
        movie_name = movie_sample_1.get_name()
        new_rating = 4.5
        
        db_manager.update_movie_rating('test_user', movie_name, new_rating)
        
        db_manager.cursor.execute("SELECT * FROM test_user WHERE name=?", (movie_name,))
        result = db_manager.cursor.fetchone()
        
        assert result is not None
        assert result[0] == movie_name
        assert result[1] == new_rating
    
    

    def test_get_movie_info(self, db_manager, movie_sample_1):
        
        db_manager.add_movie_to_user_table('test_user', movie_sample_1)
        
        movie_info = db_manager.get_user_movie_info('test_user', movie_sample_1.get_name())
        
        assert movie_info is not None
        assert movie_info.get_name() == movie_sample_1.get_name()
        assert movie_info.get_description() == movie_sample_1.get_description()
        assert movie_info.get_categories() == movie_sample_1.get_categories()
        assert movie_info.get_rating() == movie_sample_1.get_rating()
        assert movie_info.get_director() == movie_sample_1.get_director()
    