import os

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    session,
    render_template_string
)
from flask.ext.session import Session

app = Flask(__name__)


execfile('flag.py')
execfile('key.py')

FLAG = flag
app.secret_key = key


@app.route("/golem", methods=["GET", "POST"])
def golem():
    if request.method != "POST":
        return redirect(url_for("index"))

    golem = request.form.get("golem") or None

    if golem is not None:
        golem = golem.replace(".", "").replace(
            "_", "").replace("{", "").replace("}", "")

    if "golem" not in session or session['golem'] is None:
        session['golem'] = golem

    template = None

    if session['golem'] is not None:
        template = '''{% % extends "layout.html" % %}
		{% % block body % %}
		<h1 > Golem Name < /h1 >
		<div class ="row >
		<div class = "col-md-6 col-md-offset-3 center" >
		Hello: % s, why you don't look at our <a href=' / article?name = article'> article < /a >?
		< / div >
		< / div >
		{% % endblock % %}
		''' % session['golem']

        print

        session['golem'] = None

    return render_template_string(template)


@app.route('/article', methods=['GET'])
def article():
    base_path = '/home/golem/articles'
    error = 0

    page = request.args.get('name', 'article')

    # Whitelist valid filenames (no path traversal)
    allowed_files = {'article.txt', 'notallowed.txt'}  # Add safe filenames here

    # Only allow .txt files, no subdirectories, no traversal
    if '..' in page or '/' in page or '\\' in page or not page.endswith('.txt'):
        page = 'notallowed.txt'

    # Optional: full secure path check
    full_path = os.path.abspath(os.path.join(base_path, page))
    if not full_path.startswith(base_path):
        page = 'notallowed.txt'
        full_path = os.path.join(base_path, page)

    try:
        with open(full_path) as f:
            template = f.read()
    except Exception as e:
        template = str(e)

    return render_template('article.html', template=template)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
