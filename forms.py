from flask_wtf import FlaskForm
# from wtforms.ext.sqlalchemy.orm import model_form

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional


# class FashionForm(FlaskForm):
#     preference = StringField('Preference', validators=[DataRequired()])
#     body_type = StringField('Body Type', validators=[DataRequired()])
#     occasion = StringField('Occasion', validators=[DataRequired()])
#     submit = SubmitField('Get Recommendations')

class FashionForm(FlaskForm):
    preference = StringField('Preference', validators=[Optional()])
    body_type = StringField('Body Type', validators=[DataRequired()])
    occasion = StringField('Occasion', validators=[Optional()])
    submit = SubmitField('Get Recommendations')