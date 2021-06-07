from datetime import datetime

from django.urls import reverse
from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip

import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html
import resources.strings as strings
import resources.values as values


def base_button(value, href='', data_toggle='', data_target='', data_dismiss='', form='',
                type='button', extra_classes='btn-primary btn-lg py-3 w-100 border'):
    return bootstrap.btn(
        value=value,
        href=href,
        extra_classes=extra_classes,
        data_toggle=data_toggle,
        data_target=data_target,
        data_dismiss=data_dismiss,
        form=form,
        type=type
    )


# todo: strings still need to be moved from some of these functions
# delivery menu buttons
def add_order():
    # todo: pop up modal with forms related to order info
    return base_button(
        value=strings.add_order.format(html.br),
        data_toggle=values.modal_data_toggle,
        data_target=values.add_order_modal_id.format('#')
    )


def end_delivery(delivery):
    return base_button(
        value=strings.end_delivery.format(html.br),
        data_toggle=values.modal_data_toggle,
        data_target=values.end_delivery_modal_id.format('#')
    )


# main menu buttons
def shift():
    # todo: add text and url change, incase of returning from split

    shifts_list = Shift.objects.filter(date=datetime.now().date())
    for shift in shifts_list:
        # a shift is in progress
        if shift.start_time is not None and shift.end_time is None:
            return base_button(
                value=strings.continue_shift,
                href=values.base_id_url.format(
                    reverse(values.shift_menu_view),
                    values.shift_id,
                    shift.pk
                )
            )
    for shift in shifts_list:
        # at least one shift has been completed for the day
        if shift.start_time is not None and shift.end_time is not None:
            return base_button(
                value=strings.start_another_shift,
                href=reverse(values.start_shift_view)
            )

    # no shifts started for the day
    return base_button(
        value=strings.start_shift,
        href=reverse(values.start_shift_view)
    )


def view_shifts():
    return base_button(strings.view_past_shifts)


def view_statistics():
    return base_button(strings.view_statistics)


# shift menu buttons
def add_carry_out_tip():
    return base_button(
        value=strings.add_carry_out_tip.format(html.br),
        data_toggle=values.modal_data_toggle,
        data_target=values.add_carry_out_tip_modal_id.format('#')
    )


def edit_carry_out_tip(tip):

    if tip.card != 0 and tip.cash != 0:
        string = '{}<br>{}'.format(
            strings.edit_card_tip_button_text.format(tip.card),
            strings.edit_cash_tip_button_text.format(tip.cash)
        )
    elif tip.card != 0:
        string = strings.edit_card_tip_button_text.format(tip.card)
    elif tip.cash != 0:
        string = strings.edit_cash_tip_button_text.format(tip.cash)

    return base_button(
        value=string,
        data_toggle=values.modal_data_toggle,
        data_target=values.edit_carry_out_tip_modal_id.format(
            symbol='#',
            id=tip.pk
        ),
        extra_classes=values.edit_buttons_extra_classes
    )


def edit_delivery(delivery):
    return base_button(
        value=strings.delivery_id_number.format(delivery.daily_id + 1),
        data_toggle=values.modal_data_toggle,
        data_target=values.edit_delivery_modal_id.format(
            symbol='#',
            id=delivery.pk
        ),
        extra_classes=values.edit_buttons_extra_classes
    )


def edit_split(split):
    return base_button(
        value=strings.edit_split_button_value.format(split.daily_id + 1),
        data_toggle=values.modal_data_toggle,
        data_target=values.edit_split_modal_id.format(symbol='#', id=split.pk),
        extra_classes=values.edit_buttons_extra_classes
    )


def end_shift():
    return base_button(
        value=strings.end_shift.format(html.br),
        data_toggle=values.modal_data_toggle,
        data_target=values.end_shift_modal_id.format('#')
    )


def split(shift, split=None):
    if split is not None:
        # split is in progress
        if split.start_time is not None and split.end_time is None:
            return base_button(
                value=strings.end_split.format(html.br),
                data_toggle=values.modal_data_toggle,
                data_target=values.end_split_modal_id.format('#')
            )

    return base_button(
        value=strings.start_split,
        href=values.base_id_url.format(
            reverse(values.start_split_view),
            values.shift_id,
            shift.pk
        )
    )


def start_delivery(shift):
    for delivery in Delivery.objects.filter(shift_id=shift.pk):
        # a delivery is in progress
        if delivery.start_time is not None and delivery.end_time is None:
            return base_button(
                value=strings.continue_delivery,
                href=values.base_id_url.format(
                    reverse(values.delivery_menu_view),
                    values.delivery_id,
                    delivery.pk
                )
            )

    # no delivery in progress
    return base_button(
        value=strings.start_delivery,
        href=values.base_id_url.format(
            reverse(values.start_delivery_view),
            values.shift_id,
            shift.pk
        )
    )


# shared menu buttons
def add(form):
    return bootstrap.btn(
        value=strings.add_button_text,
        type=values.submit_button_type,
        extra_classes=values.bootstrap_button_primary,
        form=form
    )


def end(form):
    return bootstrap.btn(
        value=strings.end_button_text,
        type=values.submit_button_type,
        extra_classes=values.bootstrap_button_primary,
        form=form
    )


def edit_extra_stop(extra_stop, request):
    value = strings.edit_extra_stop_button_text.format(
        location=extra_stop.location,
        reason=extra_stop.reason
    )
    
    if extra_stop.delivery is not None\
            and values.delivery_id not in request.GET:
        value += '{}{}'.format(
            html.br,
            html.italicize(
                strings.delivery_id_number.format(
                    extra_stop.delivery.daily_id + 1
                )
            )
        )

    return base_button(
        value=value,
        data_toggle=values.modal_data_toggle,
        data_target=values.edit_extra_stop_modal_id.format(
            symbol='#',
            id=extra_stop.pk
        ),
        extra_classes=values.edit_buttons_extra_classes
    )


def edit_order(order, request):
    value = f'#{ order.daily_id }'

    if values.shift_id in request.GET:
        value += ' - {}'.format(html.italicize(
            strings.delivery_id_number.format(order.delivery.daily_id + 1)
        ))

    return base_button(
        value=value,
        data_toggle=values.modal_data_toggle,
        data_target=values.edit_order_modal_id.format(
            symbol='#',
            id=order.pk
        ),
        extra_classes=values.edit_buttons_extra_classes
    )


def extra_stop(parent):
    # shift
    if isinstance(parent, Shift):
        for extra_stop in ExtraStop.objects.filter(shift=parent):
            # extra stop in progress
            if extra_stop.end_time is None:
                return base_button(
                    value=strings.end_extra_stop.format(html.br),
                    data_toggle=values.modal_data_toggle,
                    data_target=values.add_extra_stop_modal_id.format('#')
                )

        # extra stop has not been started
        return base_button(
            value=strings.start_extra_stop,
            href=values.base_id_url.format(
                reverse(values.start_extra_stop_view),
                values.shift_id,
                parent.pk
            )
        )

    # delivery
    elif isinstance(parent, Delivery):
        return base_button(
            value=strings.add_extra_stop.format(html.br),
            data_toggle=values.modal_data_toggle,
            data_target=values.add_extra_stop_modal_id.format('#')
        )


def save(form):
    return bootstrap.btn(
        value=strings.save_button_text,
        type=values.submit_button_type,
        extra_classes=values.bootstrap_button_primary,
        form=form
    )
