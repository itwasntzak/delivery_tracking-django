
# todo: add string checking/formating for proper html indentions/formating
br = '<br>\n'


def a(content, href):
    return f'<a href="{ href }">{ content }</a>\n'


class Button:
    def __init__(self, value, type='button', classes = None,
                 aria_label = None, form = None):
        self.value = value
        self.type = type
        self.classes = classes
        self.aria_label = aria_label
        self.form = form

    def get_attributes(self) -> list:
        return [attr for attr in dir(self) if not
                callable(getattr(self, attr)) and not
                attr.startswith("__") and
                eval(f'self.{attr}') is not None]
    
    def get_classes(self) -> str:
        # todo: reread artical on getters, setters, properties

        if type(self.classes) is not list:
            raise TypeError('Button.classes needs to be a list')
        if len(self.classes) < 1:
            raise ValueError(
                'Button.classes needs to contain at least one string'
            )
        for item in self.classes:
            if type(item) is not str:
                raise TypeError(
                    'Button.classes item must be string of class names\n'
                    'instance of Button.classes item at index: '
                    f'{self.classes.index(item)}'
                )

        classes = ''
        for html_class in self.classes:
            classes += html_class
            if html_class != self.classes[-1]:
                classes += ' '
        return classes

    def start_html(self, attributes, classes) -> str:
        # have to add the '>' to the end of the returned string

        html = '<button '
        for attribute in attributes:
            if '_' in attribute:
                attribute.replace('_', '-')

            if attribute == 'classes' and classes != []:
                html += f'{attribute}="{classes}"'
                if attribute != attributes[-1]:
                    html += ' '
            elif attribute != 'classes' and eval(f'self.{attribute}') != '':
                html += f'{attribute}="{eval(f"self.{attribute}")}"'
                if attribute != attributes[-1]:
                    html += ' '
        return html

    def full_html(self, start_html) -> str:
        return f'{ start_html }>{ self.value }</button>'


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

    html + f'>{ content }</div>\n'

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