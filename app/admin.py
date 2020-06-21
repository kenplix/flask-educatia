from flask import redirect, url_for, request, abort
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        return redirect(url_for('auth.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass
