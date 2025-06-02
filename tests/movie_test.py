from src.movie import Movie
import pytest

@pytest.fixture
def movie_sample_1():
    name = 'Movie 1 test name'
    description = 'This is a test movie with no categories assigned'
    categories = []
    rating = 2.5
    director = 'Test author'

    return Movie(name,description,categories,rating,director)

@pytest.fixture
def movie_sample_multiple_categories():
    name = 'Multiple categories movie'
    description = 'Test movie with more than one category assigned'
    categories = ['Test Category One','Test Category Two','Test Category Three']
    rating = 2.5
    director = 'Test author'

    return Movie(name,description,categories,rating,director)

class TestMovie:

    def test_create_movie_with_empty_categories_list(self,movie_sample_1):
        assert movie_sample_1 != None
    
    def test_create_movie_with_one_category(self):

        name = 'Movie 2 test name'
        description = 'This is a test movie with one category assigned'
        categories = ['Test Category']
        rating = 2.5
        director = 'Test author'
        
        assert Movie(name,description,categories,rating,director) != None
    
    def test_create_movie_with_multiple_categories(self,movie_sample_multiple_categories):
        assert movie_sample_multiple_categories != None

    def test_get_name(self,movie_sample_1):
        assert movie_sample_1.get_name() == 'Movie 1 test name'
    
    def test_get_description(self,movie_sample_1):
        assert movie_sample_1.get_description() == 'This is a test movie with no categories assigned'

    def test_get_empty_categories(self,movie_sample_1):
        assert movie_sample_1.get_categories() == []

    def test_get_multiple_categories(self,movie_sample_multiple_categories):
        assert movie_sample_multiple_categories.get_categories() == ['Test Category One','Test Category Two','Test Category Three']

    def test_get_rating(self,movie_sample_1):
        assert movie_sample_1.get_rating() == 2.5

    def test_get_director(self,movie_sample_1):
        assert movie_sample_1.get_director() == 'Test author'