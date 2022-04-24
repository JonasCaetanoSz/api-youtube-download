from api import API
import os

port_deploy = int(os.environ.get("PORT", 5000)) # porta para deploy no heroku.


if __name__ == "__main__":

    server = API()
    server.start(debug=False, port=port_deploy , host="0.0.0.0")
