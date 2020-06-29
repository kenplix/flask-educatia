from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from app.wysiwyg import CKTextAreaField


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    content = CKTextAreaField(
        'Content',
        validators=[DataRequired()]
    )

    tags = StringField(
        'Tags',
        validators=[Optional()]
    )

    submit = SubmitField('Post')
