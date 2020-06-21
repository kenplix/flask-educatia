'''

Create error handlers with their own templates for each of the status
codes we care about.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from flask import render_template


def error_templates(app):
    '''
    Register 0 or more custom error pages. Note that this function mutates the
    provided 'app' parameter.
    :param app: Flask application instance
    '''

    def render_status(status):
        '''
        Render a custom template for a specific status.
          Source: http://stackoverflow.com/a/30108946
        :param status: Status as a written name
        :return:       None
        '''

        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template(f'errors/{code}.html'), code

    # Iterate through each error code we have decided to create error pages
    # for, and create their respective error handlers.
    for error in [403, 404, 500]:
        app.errorhandler(error)(render_status)
