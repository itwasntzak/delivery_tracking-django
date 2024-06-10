import resources.strings as strings
import resources.values as values
import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html
import py_web_ui.html as html
import py_web_ui.strings as html_strings

def average_speed(object=None, value=''):
    if object is not None:
        value = object.average_speed

    return bootstrap.field(
        label=strings.average_speed_field_label,
        input_type=values.number_field_input_type,
        id=values.average_speed_field_id,
        value=value,
        step=values.number_field_step_by_point_zero_one,
        min=0,
        required=True
    )


def device_compensation(shift=None, value=''):
    if shift is not None:
        value = shift.device_compensation

    return bootstrap.field(
        label=strings.device_compensation_field_label,
        input_type=values.number_field_input_type,
        id=values.device_compensation_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


def distance(object=None, value=''):
    if object is not None:
        value = object.distance

    return bootstrap.field(
        label=strings.distance_field_label,
        input_type=values.number_field_input_type,
        id=values.distance_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


def end_time(object=None, value=''):
    # todo: fix formating of time to be able to pass to time input

    if object is not None:
        # error will occur if an object is passed in without a end time
        value = object.end_time.strftime('%H:%M')

    return bootstrap.field(
        label=strings.end_time_field_label,
        input_type=html_strings.time_field_input_type,
        id=values.end_time_field_id,
        value=value,
        required=True
    )


def extra_tips_claimed(shift=None, value=''):
    if shift is not None:
        value = shift.extra_tips_claimed

    return bootstrap.field(
        label=strings.extra_tips_claimed_field_label,
        input_type=values.number_field_input_type,
        id=values.extra_tips_claimed_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


def fuel_economy(shift=None, value=''):
    if shift is not None:
        value = shift.fuel_economy
    
    return bootstrap.field(
        label=strings.fuel_economy_field_label,
        input_type=values.number_field_input_type,
        id=values.fuel_economy_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


def location(extra_stop=None, value=''):
    if extra_stop is not None:
        value = extra_stop.location

    return bootstrap.field(
        label=strings.location_field_lable,
        input_type=html_strings.text_field_input_type,
        id=values.location_field_id,
        value=value,
        required=True
    )


def note(split=None, value=''):
    if split is not None:
        value = split.note

    return bootstrap.field(
        label=strings.note_field_label,
        input_type=values.text_field_input_type,
        id=values.note_field_id,
        value=value
    )


def order_daily_id(order=None, value=''):
    if order is not None:
        value = order.daily_id

    return bootstrap.field(
        label=strings.order_id_field_label,
        input_type=values.number_field_input_type,
        id=values.daily_id_field_id,
        value=value,
        min=0,
        required=True
    )


def reason(extra_stop=None, value=''):
    if extra_stop is not None:
        value = extra_stop.reason

    return bootstrap.field(
        label=strings.reason_field_label,
        input_type=html_strings.text_field_input_type,
        id=values.reason_field_id,
        value=value,
        required=True
    )


def recorded_hours(shift=None, value=''):
    if shift is not None:
        value = shift.recorded_hours
    
    return bootstrap.field(
        label=strings.recorded_hours_field_label,
        input_type=values.number_field_input_type,
        id=values.recorded_hours_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


def sending_menu(value):
    return html.input_tag(
        input_type=html_strings.hidden_field_input_type,
        name=values.sending_menu_field_id,
        value=value
    )


def start_time(object=None, value=''):
    # todo: fix formating of time to be able to pass to time input

    if object is not None:
        # error will occur if an object is passed in without a start time
        value = object.start_time.strftime('%H:%M')

    return bootstrap.field(
        label=strings.start_time_field_label,
        input_type=html_strings.time_field_input_type,
        id=values.start_time_field_id,
        value=value,
        required=True
    )


def tip(tip=None, card_value=0.0, cash_value=0.0):
    if tip is not None:
        card_value = tip.card
        cash_value = tip.cash

    return '\n'.join([
        bootstrap.field(
            label=strings.card_field_label.format(''),
            input_type=values.number_field_input_type,
            id=values.card_field_id,
            value=card_value,
            step=.01,
            required=True
        ),
        bootstrap.field(
            label=strings.cash_field_label.format(''),
            input_type=values.number_field_input_type,
            id=values.cash_field_id,
            value=cash_value,
            step=.01,
            required=True
        )
    ])


def vehicle_compensation(shift=None, value=''):
    if shift is not None:
        value = shift.vehicle_compensation

    return bootstrap.field(
        label=strings.vehicle_compensation_field_label,
        input_type=values.number_field_input_type,
        id=values.vehicle_compensation_field_id,
        value=value,
        step=values.number_field_step_by_any,
        min=0,
        required=True
    )


# composite fields
def add_extra_stop(extra_stop=None):
    fields = [
        location(),
        reason(),
        distance(),
    ]
    # start time
    if extra_stop is not None and extra_stop.shift is not None:
        fields.insert(0, start_time(extra_stop))

    return fields


def add_order():
    return [
        order_daily_id(),
        distance(),
        tip()
    ]


def edit_delivery(delivery):
    return [
        start_time(delivery),
        end_time(delivery),
        distance(delivery),
        average_speed(delivery)
    ]


def edit_extra_stop(extra_stop, request):
    fields = [
        end_time(extra_stop),
        location(extra_stop),
        reason(extra_stop),
        distance(extra_stop)
    ]
    # start time
    if extra_stop.shift is not None:
        fields.insert(0, start_time(extra_stop))

    # add hidden input field to know what menu to return the user to
    if values.shift_id in request.GET:
        fields.append(sending_menu('s'))
    elif values.delivery_id in request.GET:
        fields.append(sending_menu('d'))
    
    return fields


def edit_order(order, order_tip, request):
    fields = [
        order_daily_id(order),
        end_time(order),
        distance(order),
        tip(order_tip)
    ]

    # add hidden input field to know what menu to return the user to
    if values.shift_id in request.GET:
        fields.append(sending_menu('s'))
    elif values.delivery_id in request.GET:
        fields.append(sending_menu('d'))
    
    return fields


def end_delivery(delivery):
    return [
        start_time(delivery),
        distance(),
        average_speed()
    ]


def end_shift(shift):
    return [
        start_time(shift),
        distance(),
        fuel_economy(),
        recorded_hours(),
        vehicle_compensation(),
        device_compensation(),
        extra_tips_claimed()
    ]


def split(split=None, end=False, edit=False):
    # end
    if end is True and split is not None:
        return [
            # start time
            start_time(split),
            # distance
            distance(),
            # note
            note()
        ]
    # edit
    elif edit is True and split is not None:
        return [
            start_time(split),
            end_time(split),
            distance(split),
            note(split)
        ]
    
    return ''
