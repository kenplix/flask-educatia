from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKEditor(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', 'editor')
        return super(CKEditor, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditor()
