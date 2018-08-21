def Articles():
    articles = [
        {
            'id': 1,
            'recipe_name':'chocolate chip cookies',
            'ingredients':['salt','papper'],
            'instructions': [{1: 'dosomething', 2: 'dosomething else'}],
            'serving_size': 2,
            'category': 'sweet',
            'notes': ['add hot water', 'let it cooldown'],
            'author':'Meet',
            'date_added':'08-13-2018',
            'date_modified':'08-13-2018'
        },
        {
            'id': 2,
            'recipe_name':'cake dough cookies',
            'ingredients':['salt','papper'],
            'instructions': [{1: 'dosomething', 2: 'dosomething else'}],
            'serving_size': 2,
            'category': 'sweet',
            'notes': ['add hot water', 'let it cooldown'],
            'author':'Meet',
            'date_added':'08-13-2018',
            'date_modified':'08-13-2018'
        },
        {
            'id': 3,
            'recipe_name':'cookies',
            'ingredients':['salt','papper'],
            'instructions': [{1: 'dosomething', 2: 'dosomething else'}],
            'serving_size': 2,
            'category': 'sweet',
            'notes': ['add hot water', 'let it cooldown'],
            'author':'Meet',
            'date_added':'08-13-2018',
            'date_modified':'08-13-2018'
        }
    ]
    
    user = [
        {
            'id': 1,
            'user_name':'jeff',
            'email': 'jeff@yahoo.com',
            'password': 'xyz',
        },
        {
            'id': 1,
            'user_name':'meet',
            'email':'meet@gmail.com',
            'password': 'abc',
        }
    ]
    return articles
