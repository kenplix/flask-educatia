from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    content = CKEditorField(
        'Content',
        validators=[DataRequired()]
    )

    tags = StringField(
        'Tags',
        validators=[Optional()]
    )

    submit = SubmitField('Post')
