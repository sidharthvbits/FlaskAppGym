from flask import Flask
from flask import render_template, request, flash, redirect, url_for
# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'test-secret_key'

def validate_donation_amount(amount):
    """
    Validate donation amount
    Returns tuple (is_valid, error_message)
    """
    try:
        amount = float(amount)
        if amount < 1:
            return False, "Donation amount must be at least $1"
        elif amount > 100:
            return False, "Donation amount cannot exceed $100"
        else:
            return True, None
    except (ValueError, TypeError):
        return False, "Please enter a valid number"


@app.route('/blog')
def blog():
    # Sample blog posts
    blog_posts = [
        {
            "title": "Yoga Anatomy",
            "content": "An in-depth look at the anatomy of yoga poses, helping practitioners understand their bodies better.",
            "date": "2011-01-01",
            "author": "Leslie Kaminoff"
        },
        {
            "title": "The New Rules of Lifting",
            "content": "A strength training program that focuses on building muscle and losing fat through effective workouts.",
            "date": "2005-01-01",
            "author": "Lou Schuler & Alwyn Cosgrove"
        },
        {
            "title": "Yoga for Beginners",
            "content": "A beginner-friendly guide to starting a yoga practice, including basic poses and breathing techniques.",
            "date": "2010-01-01",
            "author": "Barbara Benagh"
        }
    ]
    return render_template('blog.html', posts=blog_posts)


@app.route('/donate', methods=['POST'])
def process_donation():
    amount = request.form.get('amount', '')

    is_valid, error_message = validate_donation_amount(amount)

    if not is_valid:
        flash(error_message, 'error')
        return redirect(url_for('blog'))

    # If validation passes
    flash(f'Thank you for your donation of ${float(amount):.2f}! Your support helps keep this blog free.', 'success')
    return redirect(url_for('blog'))


# Define route for home/root URL
@app.route('/')
def home():
    return render_template('home.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
