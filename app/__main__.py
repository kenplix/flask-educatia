"""

Defines a file to run an application as a module.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

"""

from . import create_app

app = create_app()

app.run()
