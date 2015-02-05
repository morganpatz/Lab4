from flask import Flask
# only use __name__ when its just one file
# if its a package, use the package name
app = Flask(__name__)
# if this is added to the end of a url, the next method should be run
@app.route('/hello')
def hello():
    return '<h1>Hello Flask!</h1>'

@app.route('/second')
@app.route('/second/<name>')
def hello2(name = 'FLASK'):
    return '<h1>Hello %s (second test)!</h1>' % name

if __name__ == '__main__':
    app.run()
    