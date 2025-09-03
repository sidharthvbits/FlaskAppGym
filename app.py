from flask import Flask
from flask import render_template, request
# Create Flask application instance
app = Flask(__name__)

# Define route for home/root URL
@app.route('/')
def home():
    return render_template('home.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
