import development as development
from flask import Flask


app = Flask(__name__)
app.config['Environment'] = development
app.config['TESTING'] = True
app.config['debug'] = True


@app.route('/')
def index():
    return 'Index me'


if __name__ == '__main__':
    app.run(port=5000, debug=True)