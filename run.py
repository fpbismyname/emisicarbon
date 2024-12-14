import sys
from app import create_app

app = create_app()
sys.dont_write_bytecode = True

if __name__ == "__main__":
    app.run(debug=True)