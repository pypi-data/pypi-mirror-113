# flask-error-templating

Create Flask HTTP error handlers that use template rendering. This is a very small and simple idea but I couldn't find anything like it so I made it myself.

## Installation

Install with `pip install flask-error-templating`

## Usage

```python
create_http_error_handlers(app, error_pages, page_template_file)
```

`app` is a handle to your `Flask` object.

`error_pages` is a list of `ErrorPage` objects. It accepts three arguments: `error_code`, `message` and `long_message`. `error_code` and `message` are required; `long_message` is optional and if it is not present then it will not be rendered into the template.

`page_template_file` is the filename of a HTML file in your projects `templates` folder. Parameters supplied to the file for template rendering are `error_code`, `message` and `long_message`. See the above paragraph for information on these parameters.

#### Complete basic example:
```python
from flask import *
from flask_error_templating import ErrorPage, create_http_error_handlers

app = Flask(__name__)

@app.route('/')
def homepage():
    return '<h1>Homepage</h1>'

error_pages = [
    ErrorPage(400, 'Bad request'),
    ErrorPage(400, 'Access is denied to this page.'),
    ErrorPage(403, 'You are forbidden to view this page.'),
    ErrorPage(404, 'The page you are looking for does not exist'),
    ErrorPage(418, 'I\'m a teapot!')
]
create_http_error_handlers(app, error_pages, 'http_error.html')

if __name__ == '__main__':
    app.run()

```