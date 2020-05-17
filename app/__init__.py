from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from config import Config
from redis import Redis
import rq
import logging
from logging.handlers import RotatingFileHandler
import os

bootstrap = Bootstrap()

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	bootstrap.init_app(app)
	#
	app.redis = Redis.from_url(app.config['REDIS_URL'])
	app.task_queue = rq.Queue('analysis_tasks', connection = app.redis)

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	if not os.path.exists('logs'):
		os.mkdir('logs')

	file_handler = RotatingFileHandler('logs/mySentimentAnalytics.log', maxBytes=10240, backupCount=10)

	file_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s [in %(pathname)s : %(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('mySentimentAnalytics ha iniciado con exito!')

	#print("instancia de app creada")
	return app
