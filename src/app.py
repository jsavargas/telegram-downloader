import time
import os

from controllers.configs import *

from flask import Flask
from routes.index import index
#from routes.detail import detail
#from routes.config import config

app = Flask(__name__)


app.secret_key = b'@Rh8Ws#yBbW5@uYh^L^8*QGNnmLkpW*KWi'

app.register_blueprint(index)
#app.register_blueprint(detail)
#app.register_blueprint(config)


if os.path.isfile(LOCKFILE):
    os.remove(LOCKFILE)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
