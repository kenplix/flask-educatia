"""

Defines a hook for easy receiving blueprints

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

"""

from .auth.routes import auth
from .main.routes import main
from .posts.routes import posts
from .users.routes import users

blueprints = [
    auth,
    main,
    posts,
    users
]
