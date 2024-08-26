import os
import sys


print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

# Add the current directory to the Python path
sys.path.append(os.getcwd())

try:
    from app import create_app
    print("Successfully imported create_app")
except ImportError as e:
    print("Failed to import create_app:", str(e))
    print("Contents of app directory:", os.listdir('app'))
    with open('app/__init__.py', 'r') as f:
        print("Contents of app/__init__.py:", f.read())

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)