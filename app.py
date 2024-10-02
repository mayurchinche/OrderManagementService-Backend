from src import create_app
from src.firebase.service import *

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
