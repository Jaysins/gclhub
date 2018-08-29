from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def index():
    """
    index
    """
    return render_template('index.html')


@app.route('/signup')
def signup():
    """
    Signup
    """    
    if request.method == 'POST':
        return
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
