from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:

    def __init__(self, data):

        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def create_new(data):
        query = '''INSERT INTO recipes ( name, description, instructions, date_made, under_30, user_id, created_at, updated_at ) 
                VALUES ( %(name)s , %(desc)s , %(inst)s , %(date)s , %(under)s , %(uid)s , NOW() , NOW() );
                '''
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def edit(data):
        query = '''UPDATE recipes SET name = %(name)s, description = %(desc)s, instructions = %(inst)s, 
                date_made = %(date)s, under_30 = %(under)s, updated_at = NOW() WHERE id = %(id)s;
                '''
        return connectToMySQL('recipes').query_db(query, data)
    
    @staticmethod
    def delete(data):
        query = '''
                DELETE FROM recipes WHERE id = %(id)s;
                '''
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        if results:
            for recipe in results:
                recipes.append(cls(recipe))
            return recipes
        else:
            print("No results")
