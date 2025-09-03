from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Define route for home/root URL
@app.route('/')
def home():
    return '<h1>Hello</h1>'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
