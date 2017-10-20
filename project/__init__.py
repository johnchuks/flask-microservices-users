from flask import Flask, jsonify
from project.config import DevelopmentConfig


#instantiate the application
app = Flask(__name__)

#set config
app.config.from_object(DevelopmentConfig)

@app.route('/ping', methods=['GET'])
def ping_pong():
  return jsonify({
    'status':'success',
    'message': 'pong!'
  })
