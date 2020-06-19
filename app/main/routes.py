from flask import render_template, redirect, url_for, request, current_app
from app.main.forms import RequestAnalysisForm
from app.main import bp
from app.analytics import pipelineAnalytics

# Routes file enlaza una URL a función(es)

"""
def launch_task(name, *args, **kwargs):
    rq_job = current_app.task_queue.enqueue('app.analytics.' + name, *args, **kwargs)
"""

# Vistas: /, /index
@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
def index():
    print('begin :v')

    keysL = list()
    positiveL = list()
    negativeL = list()
    
    # Ejecución default
    #(keysL, positiveL, negativeL) = pipelineAnalytics()

    # Validación del formulario
    form = RequestAnalysisForm()
    if form.validate_on_submit():

        # Ejecución a petición del usuario
        (keysL, positiveL, negativeL) = pipelineAnalytics()
        print(keysL)
        print(positiveL)
        print(negativeL)

    return render_template('index.html', title = 'Sentiment Analytics', form = form, keysL=keysL, positiveL=positiveL, negativeL=negativeL)
