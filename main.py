from app_core import app
from application.functions import *

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000,debug=True)