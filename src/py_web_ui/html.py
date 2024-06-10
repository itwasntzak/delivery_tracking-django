
# todo: add string checking/formating for proper html indentions/formating
br = '<br>\n'


def a(content, href):
    return f'<a href="{ href }">{ content }</a>\n'


def button(value, type='button', classes='', data_toggle='', data_target='',
           data_dismiss='', aria_label='', form=''):

    html = '<button'

    if type != '':
        html += f' type="{ type }"'
    if classes != '':
        html += f' class="{ classes }"'
    if data_toggle != '':
        html += f' data-bs-toggle="{ data_toggle }"'
    if data_target != '':
        html += f' data-bs-target="{ data_target }"'
    if data_dismiss != '':
        html += f' data-dismiss="{ data_dismiss }"'
    if aria_label != '':
        html += f' aria-label="{ aria_label }"'
    if form != '':
        html += f' form="{ form }"'

    html += f'>{ value }</button>\n'

    return html


def div(content, classes='', style='', id='', tabindex='', role='',
        aria_label='', aria_labelledby='', aria_hidden=''):

    html = '<div'

    if classes != '':
        html += f' class="{ classes }"'
    if style != '':
        html += f' style="{ style }"'
    if id != '':
        html += f' id="{ id }"'
    if tabindex != '':
        html += f' tabindex="{ tabindex }"'
    if role != '':
        html += f' role="{ role }"'
    if aria_label != '':
        html += f' aria-label="{ aria_label }"'
    if aria_labelledby != '':
        html += f' aria-labelledby="{ aria_labelledby }"'
    if aria_hidden != '':
        html += f' aria-hidden="{ aria_hidden }"'

    html += f'>{ content }</div>\n'

    return html


def form(content, method, action='', id=''):

    html = f'<form action="{ action }" method="{ method }"'
    if id != '':
        html += f' id="{id}"'
    
    html += f'>{ content }</form>\n'

    return html


def h1(content, classes='', id=''):

    html = '<h1'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }'

    html += f'>{ content }</h1>\n'

    return html


def h2(content, classes='', id=''):

    html = '<h2'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }'

    html += f'>{ content }</h2>\n'

    return html


def h3(content, classes='', id=''):

    html = '<h3'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }'

    html += f'>{ content }</h3>\n'

    return html


def h4(content, classes='', id=''):

    html = '<h4'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }'

    html += f'>{ content }</h4>\n'

    return html


def h5(content, classes='', id=''):

    html = '<h5'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }'

    html += f'>{ content }</h5>\n'

    return html


def input_tag(input_type, classes='', id='', name='', value='', step='', min='',
              max='', required=False):

    html = f'<input type="{ input_type }"'
    if classes != '':
        html += f' class="{ classes }"'
    if id != '':
        html += f' id="{ id }"'
    if name != '':
        html += f' name="{ name }"'
    if value != '':
        html += f' value="{ value }"'
    if step != '':
        html += f' step="{ step }"'
    if min != '':
        html += f' min="{ min }"'
    if max != '':
        html += f' max="{ max }"'
    if required is True:
        html += f' required'

    html += '>\n'

    return html


def italicize(text):
    return f'<i>{text}</i>\n'


def label(content, to, classes=''):

    html = f'<label for="{ to }"'
    if classes != '':
        html += f' class="{ classes }"'
    
    html += f'>{ content }</label>\n'

    return html


def span(content, aria_hidden=''):
    return f'<span aria-hidden="{ aria_hidden }">{ content }</span>\n'