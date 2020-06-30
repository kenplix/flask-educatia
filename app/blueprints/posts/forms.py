from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from app.wysiwyg import CKEditorField


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    content = CKEditorField(
        'Content',
    )

    tags = StringField(
        'Tags',
        validators=[Optional()]
    )

    submit = SubmitField('Post')
