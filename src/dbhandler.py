import os
from dbhandler_mysql import save_to_database as save_to_database_mysql
from dbhandler_sqllite import save_to_database as save_to_database_sqllite

def save_to_database(input_text, generated_text):
    database_handlers = {
        'mysql': save_to_database_mysql,
        'sqllite': save_to_database_sqllite
    }

    use_database = os.environ.get('DB_NAME', 'sqllite')

    print("use_database-->",use_database)

    if use_database not in database_handlers:
        print(f"Error: Invalid database name '{use_database}'")
        return None

    try:
        print("database-->",use_database)
        save_function = database_handlers[use_database]
        save_function(input_text, generated_text)
    except Exception as e:
        print(f"Error in saving to database: {e}")
        return None
