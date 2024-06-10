from django.urls import reverse
from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip

import resources.strings as strings
import resources.values as values
import ui.elements.forms as forms
import ui.elements.buttons as buttons
import ui.elements.fields as fields
import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html

def add_carry_out_tip(form, add_button):
    return bootstrap.modal(
        id=values.add_carry_out_tip_modal_id.format(''),
        label=values.add_carry_out_tip_modal_label,
        title=strings.add_carry_out_tip.format(' '),
        body_content=form,
        footer_content=add_button
    )


def add_extra_stop(form, add_button):
    return bootstrap.modal(
        id=values.add_extra_stop_modal_id.format(''),
        label=values.add_extra_stop_modal_label,
        title=strings.add_extra_stop.format(' '),
        body_content=form,
        footer_content=add_button
    )


def add_order(form, add_button):
    return bootstrap.modal(
        id=values.add_order_modal_id.format(''),
        label=values.add_order_modal_label,
        title=strings.add_order.format(' '),
        body_content=form,
        footer_content=add_button
    )


def edit_carry_out_tip(tip, form, save_button):
    return bootstrap.modal(
        id=values.edit_carry_out_tip_modal_id.format(symbol='', id=tip.pk),
        label=values.edit_carry_out_tip_modal_label.format(tip.pk),
        title=strings.edit_carry_out_tip,
        body_content=form,
        footer_content=save_button
    )


def edit_delivery(delivery, form, save_button):
    return bootstrap.modal(
        id=values.edit_delivery_modal_id.format(symbol='', id=delivery.pk),
        label=values.edit_delivery_modal_label.format(delivery.pk),
        title=strings.edit_delivery,
        body_content=form,
        footer_content=save_button
    )


def edit_extra_stop(extra_stop, form, save_button):
    return bootstrap.modal(
        id=values.edit_extra_stop_modal_id.format(symbol='', id=extra_stop.pk),
        label=values.edit_extra_stop_modal_label.format(extra_stop.pk),
        title=strings.edit_extra_stop,
        body_content=form,
        footer_content=save_button
    )


def edit_order(order, form, save_button):
    return bootstrap.modal(
        id=values.edit_order_modal_id.format(symbol='', id=order.pk),
        label=values.edit_order_modal_label.format(order.pk),
        title=strings.edit_order,
        body_content=form,
        footer_content=save_button
    )


def edit_split(split, form, save_button):
    return bootstrap.modal(
        id=values.edit_split_modal_id.format(symbol='', id=split.pk),
        label=values.edit_split_modal_label.format(split.pk),
        title=strings.edit_split_modal_title,
        body_content=form,
        footer_content=save_button
    )


def end_delivery(delivery, form, end_button):
    return bootstrap.modal(
        id=values.end_delivery_modal_id.format(''),
        label=values.end_delivery_modal_label,
        title=strings.end_delivery.format(' '),
        body_content=form,
        footer_content=end_button
    )


def end_shift(form, end_button):
    return bootstrap.modal(
        id=values.end_shift_modal_id.format(''),
        label=values.end_shift_modal_label,
        title=strings.end_shift.format(' '),
        body_content=form,
        footer_content=end_button
    )


def end_split(form, end_button):
    return bootstrap.modal(
        id=values.end_split_modal_id.format(''),
        label=values.end_split_modal_label,
        title=strings.end_split.format(' '),
        body_content=form,
        footer_content=end_button
    )
