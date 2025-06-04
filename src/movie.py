class Movie:

    def __init__(self,movie_name:str,movie_description:str,movie_categories:list,movie_rating:float,movie_director:str):
        self.name = movie_name
        self.description = movie_description
        self.categories = movie_categories
        self.rating = movie_rating
        self.director = movie_director

    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_categories(self):
        return self.categories
    
    def get_rating(self):
        return self.rating
    
    def get_director(self):
        return self.director
    
    def get_movie_info(self):
        
        categories_print_line = ''
        for category in self.categories:
            categories_print_line = f'{categories_print_line} {category} |'
        categories_print_line = categories_print_line[:-1]

        movie_info = f"Movie name: {self.name}\nDescription: {self.description}\nCategories: {categories_print_line}\nRating: {self.rating}\nDirector: {self.director}"
        
        return movie_info
    
