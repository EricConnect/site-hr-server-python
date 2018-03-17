from restapi import app
from flask_restful import Resource, Api
from restapi import controller



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)