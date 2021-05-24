import py_web_ui.html as html

def btn(value, href='', extra_classes='', data_toggle='', data_target='',
        data_dismiss='', form='', type='button'):

    classes = 'btn'
    if extra_classes != '':
        classes += f' { extra_classes }'

    button = html.button(
        value=value,
        type=type,
        classes=classes,
        data_toggle=data_toggle,
        data_target=data_target,
        data_dismiss=data_dismiss,
        form=form
    )

    if href != '':
        return html.a(button, href)

    return button


def btn_group(content, label, extra_classes='', vertical=False):
    classes = 'btn-group'
    if vertical is True:
        classes += '-vertical'
    if extra_classes != '':
        classes += f' { extra_classes }'

    return html.div(
        content=content,
        classes=classes,
        role='group',
        aria_label=label
    )


def col(content, breakpoint='', size='', extra_classes='', style=''):

    classes = 'col'
    if breakpoint != '':
        classes += f'-{ breakpoint }'
    if size != '':
        classes += f'-{ size }'
    if extra_classes != '':
        classes += f' { extra_classes }'
    return html.div(content=content, classes=classes, style=style)


def container(content, fluid=False, extra_classes='', style=''):

    classes = 'container'
    if fluid is True:
        classes += '-fluid'
    if extra_classes != '':
        classes += f' { extra_classes }'
    return html.div(content=content, classes=classes, style=style)


def field(label, input_type, id, value='', step='', min='', max='',
          required=False):

    code = html.label(
        content=label,
        to=id,
        classes='col-form-label'
    )

    code += html.input_tag(
        input_type=input_type,
        classes='form-control',
        id=id,
        name=id,
        value=value,
        step=step,
        min=min,
        max=max,
        required=required
    )

    return code


def modal(id, label, body_content, footer_content, title='', header_content=''):
    # if title and header_content are both passed in,
    #   title becomes pointless

    if header_content == '':
        defualt_content =\
            f'<h5 class="modal-title" id="exampleModalLabel">{ title }</h5>\n'\
            '<button type="button" class="btn-close"'\
                    'data-bs-dismiss="modal" aria-label="Close"'\
            '>'\
            '</button>\n'
        header_div = html.div(
            content=defualt_content,
            classes='modal-header'
        )
    else:
        header_div = html.div(
            content=header_content,
            classes='modal-header'
        )

    body_div = html.div(
        content=body_content,
        classes='modal-body'
    )

    footer_div = html.div(
        content=footer_content,
        classes='modal-footer'
    )

    modal_centent = (header_div + body_div) + footer_div

    # dialog_div
    dialog_div = html.div(
        # content div
        content=html.div(
            content=modal_centent,
            classes='modal-content'
        ),
        classes='modal-dialog',
        role='document'
    )

    return html.div(
        content=dialog_div,
        classes='modal fade',
        id=f'{ id }',
        tabindex=-1,
        aria_labelledby=f'{ label }',
        aria_hidden='true'
    )


def row(content, extra_classes='', style=''):

    classes = 'row'
    if extra_classes != '':
        classes += f' { extra_classes }'
    return html.div(content=content, classes=classes, style=style)
