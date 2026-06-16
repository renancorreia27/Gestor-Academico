from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Gestor Acadêmico Web (Em construção)</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
