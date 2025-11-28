from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Content', validators=[DataRequired()])
    enabled = BooleanField('Показувати на сайті', default=True)
    publish_date = DateTimeLocalField('Publish date', format='%Y-%m-%dT%H:%M', validators=[], default=None)
    category = SelectField('Category', choices=[
        ('news', 'News'),
        ('publication', 'Publication'),
        ('tech', 'Tech'),
        ('other', 'Other'),
    ], default='other', validators=[])
    submit = SubmitField('Save')
