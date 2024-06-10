from django.middleware.csrf import get_token
from django.urls import reverse

import resources.values as values
import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html

def base_form(content, action, id, request):

    fields = '{}\n{}'.format(
        html.input_tag(
            input_type='hidden',
            name='csrfmiddlewaretoken',
            value=get_token(request)
        ),
        content
    )

    return html.form(
        content=fields,
        action=action,
        method='post',
        id=id
    )


def add_carry_out_tip(shift, fields, request):
    return base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.add_carry_out_tip_view),
            values.shift_id,
            shift.pk
        ),
        id=values.add_carry_out_tip_form_id,
        request=request
    )


def add_extra_stop(parent_info, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.add_extra_stop_view),
            parent_info['type'],
            parent_info['id']
        ),
        id=values.add_extra_stop_form_id,
        request=request
    )


def add_order(delivery, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.add_order_view),
            values.delivery_id,
            delivery.pk
        ),
        id=values.add_order_form_id,
        request=request
    )


def edit_carry_out_tip(tip, fields, request):
    return base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.edit_carry_out_tip_view),
            values.tip_id,
            tip.pk
        ),
        id=values.edit_carry_out_tip_form_id.format(tip.pk),
        request=request
    )


def edit_delivery(delivery, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.edit_delivery_view),
            values.delivery_id,
            delivery.pk
        ),
        id=values.edit_delivery_form_id.format(delivery.pk),
        request=request
    )


def edit_extra_stop(extra_stop, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.edit_extra_stop_view),
            values.extra_stop_id,
            extra_stop.pk
        ),
        id=values.edit_extra_stop_form_id.format(extra_stop.pk),
        request=request
    )


def edit_order(order, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.edit_order_view),
            values.order_id,
            order.pk
        ),
        id=values.edit_order_form_id.format(order.pk),
        request=request
    )


def edit_split(split, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.edit_split_view),
            values.split_id,
            split.pk
        ),
        id=values.edit_split_form_id.format(split.pk),
        request=request
    )


def end_delivery(delivery, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.end_delivery_view),
            values.delivery_id,
            delivery.pk
        ),
        id=values.end_delivery_form_id,
        request=request
    )


def end_shift(shift, fields, request):
    return base_form(
        content='\n'.join(fields),
        action=values.base_id_url.format(
            reverse(values.end_shift_view),
            values.shift_id,
            shift.pk
        ),
        id=values.end_shift_form_id,
        request=request
    )


def end_split(split, fields, request):
    if split is not None:
        return base_form(
                content='\n'.join(fields),
                action=values.base_id_url.format(
                    reverse(values.end_split_view),
                    values.split_id,
                    split.pk
                ),
                id=values.end_split_form_id,
                request=request
            )

    return ''
