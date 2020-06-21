'''

Creates error handlers with their own templates for each of the status codes.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from flask import render_template


def error_templates(app):
    '''
    Registers custom error pages. Note that this function mutates the
    provided 'app' parameter.

    :param app: Flask application instance
    '''

    def render_status(status):
        '''
        Render a custom template for a specific status.
          Source: http://stackoverflow.com/a/30108946

        :param status: Status as a written name
        :return: None
        '''

        code = getattr(status, 'code', 500)
        return render_template(f'errors/{code}.html'), code

    for error in [403, 404, 500]:
        app.errorhandler(error)(render_status)
