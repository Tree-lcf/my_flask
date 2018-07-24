from flask import Flask, request, make_response, render_template
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
