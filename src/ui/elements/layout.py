
import py_web_ui.bootstrap as bootstrap


def base_button_col(button, breakpoint='lg', size=4, extra_classes=''):
    return bootstrap.col(
        content=button,
        breakpoint=breakpoint,
        size=size,
        extra_classes=extra_classes
    )


def button_group(button_list, label):
    return bootstrap.btn_group(
        content='\n'.join(button_list),
        label=label,
        extra_classes='w-100'
    )


def button_modal_group_row_col(button_modal_group):
    return bootstrap.row(
        bootstrap.col(
            content=button_modal_group,
            size=12
        ),
        extra_classes='m-5'
    )


def two_button_row(button_1, button_2, extra_classes='mx-3 my-4 text-center'):
    return bootstrap.row(
        content='{}\n{}\n'.format(
            base_button_col(
                button_1,
                size=6
            ),
            base_button_col(
                button_2, 
                size=6
            ),
        ),
        extra_classes=extra_classes
    )


def three_button_row(button_1, button_2, button_3,
                     extra_classes='mx-3 my-4 text-center'):
    return bootstrap.row(
        content='{}\n{}\n{}\n'.format(
            base_button_col(button_1),
            base_button_col(button_2),
            base_button_col(button_3),
        ),
        extra_classes=extra_classes
    )
