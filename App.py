from flask import Flask


app = Flask(__name__)
app.config['']

app.route('/')
def index():
    return 'Parti!!'



if __name__ == '__main__':
    app.run(port=5000, debug=True)