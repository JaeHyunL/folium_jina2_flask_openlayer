from flask import Flask, render_template


app = Flask(__name__, static_url_path='/static', template_folder='template')


@app.route('/')
def main():
    value_list = ['list1', 'list2', 'list3']
    return render_template('index.html', values=value_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
