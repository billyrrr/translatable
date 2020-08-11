import flask
from flasgger import Swagger
from flask import Flask, request, abort

app = Flask(__name__)


import re

g = list()


def encode(matchobj):
    s = matchobj.group(0)
    idx = len(g)
    g.append(s)
    return "<!--{%" + str(idx) + "%}-->"


def decode(matchobj):
    k = matchobj.group(0)
    idx = int(k[6:-5])
    s = g[idx]
    return s


def _translate(text, source='en', sink='zh'):
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    result = translate_client.translate(
        text, source_language=source, target_language=sink, model='nmt', format_='html')
    res = result['translatedText']
    # print("-----text-----")
    # print(text)
    # print('======res=====')
    # print(res)
    # print('///////////////')
    return res


from functools import wraps


def translated(func):
    @wraps(func)
    def do_translate(*args, **kwargs):
        res = func(*args, **kwargs)
        res = _translate(res)
        return res
    return do_translate


def recover_md(func):
    from functools import wraps
    @wraps(func)
    def do_recover(*args, **kwargs):
        res = func(*args, **kwargs)
        import html2markdown
        rer = html2markdown.convert(res)
        return rer+'\n\n'
    return do_recover


def change(ss):
    import mistune

    class Renderer(mistune.Renderer):
        def block_code(self, code, lang=None):
            """Rendering block level code. ``pre > code``.

            :param code: text content of the code block.
            :param lang: language of the given code.
            """
            code = code.rstrip('\n')
            if not lang:
                code = mistune.escape(code, smart_amp=False)
                return '<code>%s\n</code>\n' % code
            code = mistune.escape(code, quote=True, smart_amp=False)
            return '<code class="lang-%s">%s\n</code>\n' % (
            lang, code)

    class Markdown(mistune.Markdown):

        @recover_md
        def output_list(self):
            res = super().output_list()
            res = _translate(res)
            return res

        @recover_md
        def output_paragraph(self):
            res = super().output_paragraph()
            res = _translate(res)
            return res

        @recover_md
        def output_heading(self):
            res = super().output_heading()
            res = _translate(res)
            return res

    # from renderer import MdRenderer
    # from mistune import Renderer
    markdown = Markdown(escape=False, renderer=Renderer())

    jekyll_highlight = re.compile(
        r"{% highlight *\w* *?%\}.*?{% endhighlight *\w*? *%\}", re.DOTALL
    )

    ss = jekyll_highlight.sub(encode, ss)

    # ref: https://github.com/eyeseast/python-frontmatter/blob/master/frontmatter/default_handlers.py
    # MIT License
    FM_BOUNDARY = re.compile(r'\A'+r"-{3,}\s*.*-{3,}\s*", re.DOTALL)
    ss = FM_BOUNDARY.sub(encode, ss)

    res = markdown(ss)

    RB = re.compile(r"(<!--{%).*?(%\}-->)")

    res = RB.sub(decode, res)

    # rer =
    import html

    return html.unescape(res)


ALLOWED_EXTENSIONS = {'md','markdown'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# # def upload_file():
# #     if request.method == 'POST':
# #         # check if the post request has the file part
# #         if 'file' not in request.files:
# #             abort(400)
# #         from werkzeug.datastructures import FileStorage
# #         file: FileStorage = request.files['file']
# #         # if user does not select file, browser also
# #         # submit an empty part without filename
# #         if file is None or file.filename == '':
# #             abort(400)
# #
# #         if not allowed_file(file.filename):
# #             abort(415)
# #
# #         if file and allowed_file(file.filename):
# #             res = change(file.stream.read().decode(request.content_encoding))
# #             flask.send_file()
# #
# #     return

swagger = Swagger(app)


@app.route('/translate', methods=('POST',))
def translate():
    """Translates markdown text.
    ---
    consumes:
      - text/plain

    parameters:
      - name: original
        in: body
        type: string
        description: original markdown text
        example: "It's very easy to make some words **bold** and other words *italic* with Markdown."
      - name: Content-Language
        in: header
        description: source language
        default: en
      - name: Accept-Language
        in: header
        description: sink language or language to translate the text to
        default: zh

    responses:
        200:
          description: translation successful
          content:
            text/plain:
                description: translated text


        """
    if request.mimetype != 'text/plain':
        abort(415)
    else:
        ss = request.get_data(as_text=True)
        res = change(ss)
        return flask.make_response(res, 200, {'Content-Type': 'text/plain'})


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
