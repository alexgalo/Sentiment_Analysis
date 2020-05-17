from flask import request 
from flask_wtf import FlaskForm
from wtforms import SubmitField

class RequestAnalysisForm(FlaskForm):
    submit = SubmitField('Iniciar')
