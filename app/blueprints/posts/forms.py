from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    content = TextAreaField(
        'Content',
        validators=[DataRequired()]
    )

    tags = StringField(
        'Tags',
        validators=[Optional()]
    )

    submit = SubmitField('Post')
