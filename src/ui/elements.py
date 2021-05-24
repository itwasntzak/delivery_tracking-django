from datetime import datetime
from django.middleware.csrf import get_token

from django.urls import reverse
from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip

import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html
import resources.values as values
import resources.strings as strings


# todo: make a carry out tip button group


# base elements
def base_button(value, href='', data_toggle='', data_target='', data_dismiss='',
                extra_classes='btn-primary btn-lg py-3 w-100 border'):
    return bootstrap.btn(
        value=value,
        href=href,
        extra_classes=extra_classes,
        data_toggle=data_toggle,
        data_target=data_target,
        data_dismiss=data_dismiss
    )


def base_button_col(button, breakpoint='lg', size=4, extra_classes=''):
    return bootstrap.col(
        content=button,
        breakpoint=breakpoint,
        size=size,
        extra_classes=extra_classes
    )


def base_form(content, action, id, csrf_token):

    fields = '{}\n{}'.format(
        html.input_tag(
            input_type='hidden',
            name='csrfmiddlewaretoken',
            value=csrf_token
        ),
        content
    )

    return html.form(
        content=fields,
        action=action,
        method='post',
        id=id
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


# main elements
def logo_bar():
    return bootstrap.row(bootstrap.col(
        content=html.div(
            content=html.h4(
                content='Delviery Tracker',
                classes='mx-4'
            ),
            classes='navbar-brand py-3',
            style='font-weight: bolder; color: #e8f1f2'
        ),
        size=12,
        extra_classes='navbar',
        style='background-color: #247ba0;'
    ))


def title_text(main_text, sub_text):
    return bootstrap.row(
        content=bootstrap.col(
            content='{}{}'.format(
                html.h1(main_text),
                html.h5(sub_text)
            ),
            size=12,
            extra_classes='text-center'
        ),
        extra_classes='mx-3 my-5',
        style='color: #13293d;'
    )


# buttons
# main menu buttons
def shift_button():
    # todo: add text and url change, incase of returning from split

    url = reverse(values.start_shift_view)
    text = strings.start_shift

    shifts = Shift.objects.filter(date=datetime.now().date())
    for shift in shifts:
        # all existing shifts have been completed
        if shift.start_time is not None and shift.end_time is not None:
            text = strings.start_another_shift
        # one of the existing shifts is still in progress
        elif shift.start_time is not None and shift.end_time is None:
            text = strings.continue_shift
            url = values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                shift.pk
            )

    return base_button(text, url)


def view_shifts_button():
    return base_button(strings.view_past_shifts)


def view_statistics_button():
    return base_button(strings.view_statistics)


# shift menu buttons
def delivery_button(shift):

    url = values.base_id_url.format(
        reverse(values.start_delivery_view),
        values.shift_id,
        shift.pk
    )
    text = strings.start_delivery

    deliveries = Delivery.objects.filter(shift_id=shift.pk)
    for delivery in deliveries:
        # one of the existing deliveries is still in progress
        if delivery.start_time is not None and delivery.end_time is None:
            text = strings.continue_delivery
            url = values.base_id_url.format(
                reverse(values.delivery_menu_view),
                values.delivery_id,
                delivery.pk
            )

    return base_button(text, url)


def delivery_button_group(shift, request):
    delivery_buttons = ''
    delivery_modals = ''

    delivery_list = Delivery.objects.filter(shift=shift)
    for delivery in delivery_list:
        # delivery has been finished
        if delivery.start_time is not None and delivery.end_time is not None:
            # delivery buttons
            delivery_buttons += base_button(
                value=f'Delivery #{ delivery.daily_id + 1 }',
                data_toggle='modal',
                data_target=f'#delivery{ delivery.pk }Modal',
                extra_classes='btn-primary mb-2 boarder'
            )

            # delivery modals
            delivery_modals += edit_delivery_modal(
                delivery=delivery,
                csrf_token=get_token(request),
                request=request
            )
    
    # button group
    if not len(delivery_list) > 0:
        button_group = html.h5(
            content='There are currently no deliveries.',
            classes='ps-3'
        )
    else:
        button_group = bootstrap.btn_group(
            content=delivery_buttons,
            label='Delivery Buttons',
            extra_classes='w-100',
            vertical=True
        )

    return f'{html.h2("Deliveries:")}\n<hr>\n'\
           f'{button_group}\n'\
            f'{delivery_modals}'


def carry_out_tip_button():
    return base_button(
        value=strings.add_carry_out_tip,
        data_toggle='modal',
        data_target='#addCarryOutTipModal'
    )


def end_shift_button():
    return base_button(
        value=strings.end_shift,
        data_toggle='modal',
        data_target='#endShiftModal'
    )


def shift_extra_stop_button_group(shift, request):
    # todo: make a button group for the shift menu that displays shift and
    #       delivery extra stops, make another just for deliveries in
    #       the delivery mune

    extra_stop_list = ExtraStop.objects.filter(shift=shift)
    for delivery in Delivery.objects.filter(shift=shift):
        delivery_extra_stop_list = ExtraStop.objects.filter(delivery=delivery)
        if delivery_extra_stop_list.count() > 0:
            extra_stop_list =\
                extra_stop_list.union(ExtraStop.objects.filter(shift=shift))

    buttons = ''
    modals = ''

    for extra_stop in extra_stop_list:
        if extra_stop.end_time is not None:
            if extra_stop.shift is not None:
                buttons += base_button(
                    value=f'To: { extra_stop.location }, '\
                          f'Reason: { extra_stop.reason }',
                    data_toggle='modal',
                    data_target=f'#extraStop{ extra_stop.pk }Modal',
                    extra_classes='btn-primary mb-2 boarder'
                )

                modals += edit_extra_stop_modal(
                        extra_stop=extra_stop,
                        csrf_token=get_token(request)
                    )
            elif extra_stop.delivery is not None:
                buttons += base_button(
                    value=f'<b>Delivery,</b> To: { extra_stop.location }, '\
                          f'Reason: { extra_stop.reason }',
                    data_toggle='modal',
                    data_target=f'#extraStop{ extra_stop.pk }Modal',
                    extra_classes='btn-primary mb-2 boarder'
                )

                modals += edit_extra_stop_modal(
                        extra_stop=extra_stop,
                        csrf_token=get_token(request)
                    )

    if not extra_stop_list.count() > 0:
        button_group = html.h5('There are currently no extra stops.')
    else:
        button_group = bootstrap.btn_group(
            content=buttons,
            label='Extra Stop Button',
            extra_classes='w-100',
            vertical=True
        )

    return f'{html.h2("Extra Stops:")}\n<hr>\n'\
           f'{button_group}\n'\
           f'{modals}'


def shift_order_button_group(shift, request):
    buttons = ''
    modals = ''

    order_list = []
    for delivery in Delivery.objects.filter(shift=shift):
        for order in Order.objects.filter(delivery=delivery):
            order_list.append(order)

    for order in order_list:
        # order has been finished
        if order.end_time is not None:
            # order buttons
            buttons += base_button(
                value=f'Delivery #{ order.delivery.daily_id + 1 }, '\
                      f'#{ order.daily_id }',
                data_toggle='modal',
                data_target=f'#order{ order.pk }Modal',
                extra_classes='btn-primary mb-2 boarder'
            )

            # order modals
            modals += edit_order_modal(
                order=order,
                csrf_token=get_token(request),
                request=request
            )
    
    if not len(order_list) > 0:
        button_group = html.h5(
            content='There are currently no orders.',
            classes='ps-3'
        )
    else:
        # button group
        button_group = bootstrap.btn_group(
            content=buttons,
            label='Order Buttons',
            extra_classes='w-100',
            vertical=True
        )

    return f'{html.h2("Orders:")}\n<hr>\n'\
           f'{button_group}\n'\
           f'{modals}'


def split_button(shift):

    url = values.base_id_url.format(
        reverse(values.start_split_view),
        values.shift_id,
        shift.pk
    )
    text = strings.start_split

    # split has been started
    if Split.objects.filter(shift=shift).count() == 1:
        split = Split.objects.get(shift=shift)
        # split need to be ended
        if split.start_time is not None and split.end_time is None:
            return base_button(
                value=strings.end_split,
                data_toggle='modal',
                data_target='#endSplitModal'
            )

    return base_button(text, url)


# delivery menu buttons
def add_order_button():
    # todo: pop up modal with forms related to order info
    return base_button(
        value=strings.add_order,
        data_toggle='modal',
        data_target='#addOrderModal'
    )


def end_delivery_button():
    return base_button(
        value=strings.end_delivery,
        data_toggle='modal',
        data_target='#endDeliveryModal'
    )


def delivery_order_button_group(delivery, request):
    # todo: change button value assignment based on
    #       where the group is apearing on the site
    # todo: make a modal or a sub button group function so the
    #       modal returns the user to the proper url

    buttons = ''
    modals = ''

    order_list = Order.objects.filter(delivery=delivery)
    for order in order_list:
        # order has been finished
        if order.end_time is not None:
            # order buttons
            buttons += base_button(
                value=f'#{ order.daily_id }',
                data_toggle='modal',
                data_target=f'#order{ order.pk }Modal',
                extra_classes='btn-primary mb-2 boarder'
            )

            # order modals
            modals += edit_order_modal(
                order=order,
                csrf_token=get_token(request),
                request=request
            )
    
    if not order_list.count() > 0:
        button_group = html.h5(
            content='There are currently no orders.',
            classes='ps-3'
        )
    else:
        # button group
        button_group = bootstrap.btn_group(
            content=buttons,
            label='Order Buttons',
            extra_classes='w-100',
            vertical=True
        )

    return f'{html.h2("Orders:")}\n<hr>\n'\
           f'{button_group}\n'\
           f'{modals}'


def delivery_extra_stop_button_group(delivery, request):
    # todo: make a button group for the shift menu that displays shift and
    #       delivery extra stops, make another just for deliveries in
    #       the delivery mune

    extra_stop_list = ExtraStop.objects.filter(delivery=delivery)

    buttons = ''
    modals = ''

    for extra_stop in extra_stop_list:
        if extra_stop.end_time is not None:
            buttons += base_button(
                value=f'To: { extra_stop.location }',
                data_toggle='modal',
                data_target=f'#extraStop{ extra_stop.pk }Modal',
                extra_classes='btn-primary mb-2 boarder'
            )

            modals += edit_extra_stop_modal(
                    extra_stop=extra_stop,
                    csrf_token=get_token(request)
                )

    if not extra_stop_list.count() > 0:
        button_group = html.h5('There are currently no extra stops.')
    else:
        button_group = bootstrap.btn_group(
            content=buttons,
            label='Extra Stop Button',
            extra_classes='w-100',
            vertical=True
        )

    return f'{html.h2("Extra Stops:")}\n<hr>\n'\
           f'{button_group}\n'\
           f'{modals}'


# shared buttons
def extra_stop_button(parent):
    # shift
    if isinstance(parent, Shift):
        text = strings.start_extra_stop
        url = values.base_id_url.format(
            reverse(values.start_extra_stop_view),
            values.shift_id,
            parent.pk
        )

        for extra_stop in ExtraStop.objects.filter(shift=parent):
            # extra stop in progress
            if extra_stop.end_time is None:
                return base_button(
                    value=strings.end_extra_stop,
                    data_toggle='modal',
                    data_target='#addExtraStopModal'
                )

        return base_button(text, url)

    # delivery
    elif isinstance(parent, Delivery):
        text = strings.add_extra_stop_new_line
        return base_button(
            value=text,
            data_toggle='modal',
            data_target='#addExtraStopModal'
        )


# modals
def add_carry_out_tip_modal(shift, csrf_token):
    # fields
    # card
    fields = bootstrap.field(
        label='Card Tip:',
        input_type='number',
        id='card',
        value=0.0,
        step=.01,
    )
    # cash
    fields += bootstrap.field(
        label='Cash Tip:',
        input_type='number',
        id='cash',
        value=0.0,
        step=.01,
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.add_carry_out_tip_view),
            values.shift_id,
            shift.pk
        ),
        id='addCarryOutTipForm',
        csrf_token=csrf_token
    )

    # add/submit button
    add_button = bootstrap.btn(
        value='Add',
        type='submit',
        extra_classes='btn-primary',
        form='addCarryOutTipForm'
    )

    return bootstrap.modal(
        id='addCarryOutTipModal',
        label='addCarryOutTipLable',
        title='Add Carry Out Tip',
        body_content=form,
        footer_content=add_button
    )


def add_extra_stop_modal(parent, csrf_token):
    # todo: figure out how to load time data into forms in stardard time

    # fields
    fields = ''

    # shift
    if isinstance(parent, Shift):
        object_type = values.shift_id
        object_id = parent.pk
    
        for extra_stop in ExtraStop.objects.filter(shift=parent):
            # extra stop in progress
            if extra_stop.end_time is None:

                # start time
                fields += bootstrap.field(
                    label=strings.start_time,
                    input_type='text',
                    id='start_time',
                    value=extra_stop.start_time,
                    required=True
                )

    elif isinstance(parent, Delivery):
        object_type = values.delivery_id
        object_id = parent.pk

    # location
    fields += bootstrap.field(
        label=strings.location,
        input_type='text',
        id='location',
        required=True
    )
    # reason
    fields += bootstrap.field(
        label=strings.reason,
        input_type='text',
        id='reason',
        required=True
    )
    # distance
    fields += bootstrap.field(
        label=strings.distance,
        input_type='number',
        id='distance',
        step='any',
        min=0,
        required=True
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.add_extra_stop_view),
            object_type,
            object_id
        ),
        id='addExtraStopForm',
        csrf_token=csrf_token
    )

    # add/submit button
    add_button = bootstrap.btn(
        value='Add',
        type='submit',
        extra_classes='btn-primary',
        form='addExtraStopForm'
    )

    return bootstrap.modal(
        id='addExtraStopModal',
        label='addExtraStopLabel',
        title=strings.add_extra_stop,
        body_content=form,
        footer_content=add_button
    )


def add_order_modal(delivery, csrf_token):
    # todo: change to get extra stop id from object from query list

    # fields
    # daily id
    fields = bootstrap.field(
        label='Order #:',
        input_type='number',
        id='daily_id',
        min=0,
        required=True
    )
    # distance
    fields += bootstrap.field(
        label='Current Distance:',
        input_type='number',
        id='distance',
        step='any',
        min=0,
        required=True
    )
    # tip
    # card
    fields += bootstrap.field(
        label='Card Tip:',
        input_type='number',
        id='card',
        value=0.0,
        step=.01,
    )
    # cash
    fields += bootstrap.field(
        label='Cash Tip:',
        input_type='number',
        id='cash',
        value=0.0,
        step=.01,
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.add_order_view),
            values.delivery_id,
            delivery.pk
        ),
        id='addOrderForm',
        csrf_token=csrf_token
    )

    # add/submit button
    add_button = bootstrap.btn(
        value='Add',
        type='submit',
        extra_classes='btn-primary',
        form='addOrderForm'
    )

    return bootstrap.modal(
        id='addOrderModal',
        label='addOrderLable',
        title='Add Order',
        body_content=form,
        footer_content=add_button
    )


def edit_delivery_modal(delivery, csrf_token, request):
    # fields
    # start time
    fields = bootstrap.field(
        label='Start time:',
        input_type='text',
        id='start_time',
        value=delivery.start_time,
        required=True
    )
    # end time
    fields += bootstrap.field(
        label='End time:',
        input_type='text',
        id='end_time',
        value=delivery.end_time,
        required=True
    )
    # distance
    fields += bootstrap.field(
        label='Total Distance:',
        input_type='number',
        id='distance',
        value=delivery.distance,
        step='any',
        min=0,
        required=True
    )
    # average speed
    fields += bootstrap.field(
        label='Average Speed:',
        input_type='number',
        id='average_speed',
        value=delivery.average_speed,
        min=0,
        required=True
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.edit_delivery_view),
            values.delivery_id,
            delivery.pk
        ),
        id=f'editDelivery{ delivery.pk }Form',
        csrf_token=csrf_token
    )
    body_html = f'{form}\n'

    # save/submit button
    save_button = bootstrap.btn(
        value='Save',
        type='submit',
        extra_classes='btn-primary',
        form=f'editDelivery{ delivery.pk }Form'
    )

    return bootstrap.modal(
        id=f'delivery{ delivery.pk }Modal',
        label='editDeliveryLable',
        title='Edit Delivery',
        body_content=body_html,
        footer_content=save_button
    )


def edit_extra_stop_modal(extra_stop, csrf_token):
    # todo: figure out how to load time data into forms in stardard time

    # fields
    fields = ''

    # shift
    # start time
    fields += bootstrap.field(
        label=strings.start_time,
        input_type='text',
        id='start_time',
        value=extra_stop.start_time,
        required=True
    )
    # end time
    fields += bootstrap.field(
        label=strings.end_time,
        input_type='text',
        id='end_time',
        value=extra_stop.end_time,
        required=True
    )
    # location
    fields += bootstrap.field(
        label=strings.location,
        input_type='text',
        id='location',
        value=extra_stop.location,
        required=True
    )
    # reason
    fields += bootstrap.field(
        label=strings.reason,
        input_type='text',
        id='reason',
        value=extra_stop.reason,
        required=True
    )
    # distance
    fields += bootstrap.field(
        label=strings.distance,
        input_type='number',
        id='distance',
        step='any',
        min=0,
        value=extra_stop.distance,
        required=True
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.edit_extra_stop_view),
            values.extra_stop_id,
            extra_stop.pk
        ),
        id='editExtraStopForm',
        csrf_token=csrf_token
    )

    # save/submit button
    save_button = bootstrap.btn(
        value='Save',
        type='submit',
        extra_classes='btn-primary',
        form='editExtraStopForm'
    )

    return bootstrap.modal(
        id=f'extraStop{ extra_stop.pk }Modal',
        label='editExtraStopLable',
        title='Edit Extra Stop',
        body_content=form,
        footer_content=save_button
    )


def edit_order_modal(order, request, csrf_token):
    tip = Tip.objects.get(order=order)

    # todo: this isnt finished needs further work and thinking
    # the best solution is probably to add shift_id or delivery_id to the GET
    # and then check for which one is in the get request from the view

    body_html = ''

    if values.shift_id in request.GET:
        body_html += html.input_tag(
            input_type='hidden',
            name='menu',
            value='s'
        )
    elif values.delivery_id in request.GET:
        body_html += html.input_tag(
            input_type='hidden',
            name='menu',
            value='d'
        )


    # fields
    # daily id
    body_html += bootstrap.field(
        label='Order #:',
        input_type='number',
        id='daily_id',
        value=order.daily_id,
        min=0,
        required=True
    )
    # end time
    body_html += bootstrap.field(
        label='End time:',
        input_type='text',
        id='end_time',
        value=order.end_time,
        required=True
    )
    # distance
    body_html += bootstrap.field(
        label='Current Distance:',
        input_type='number',
        id='distance',
        value=order.distance,
        step='any',
        min=0,
        required=True
    )
    # tip
    # card
    body_html += bootstrap.field(
        label='Card Tip:',
        input_type='number',
        id='card',
        value=tip.card,
        step=.01,
    )
    # cash
    body_html += bootstrap.field(
        label='Cash Tip:',
        input_type='number',
        id='cash',
        value=tip.cash,
        step=.01,
    )

    # form
    form = base_form(
        content=body_html,
        action=values.base_id_url.format(
            reverse(values.edit_order_view),
            values.order_id,
            order.pk
        ),
        id=f'editOrder{ order.pk }Form',
        csrf_token=csrf_token
    )

    # save/submit button
    save_button = bootstrap.btn(
        value='Save',
        type='submit',
        extra_classes='btn-primary',
        form=f'editOrder{ order.pk }Form'
    )

    return bootstrap.modal(
        id=f'order{ order.pk }Modal',
        label='editOrderLable',
        title='Edit Order',
        body_content=form,
        footer_content=save_button
    )


def end_delivery_modal(delivery, csrf_token):
    # fields
    # start time
    fields = bootstrap.field(
        label='Start time:',
        input_type='text',
        id='start_time',
        value=delivery.start_time,
        required=True
    )
    # distance
    fields += bootstrap.field(
        label='Total Distance:',
        input_type='number',
        id='distance',
        step='any',
        min=0,
        required=True
    )
    # average speed
    fields += bootstrap.field(
        label='Average Speed:',
        input_type='number',
        id='average_speed',
        min=0,
        required=True
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.end_delivery_view),
            values.delivery_id,
            delivery.pk
        ),
        id='endDeliveryForm',
        csrf_token=csrf_token
    )

    # end/submit button
    end_button = bootstrap.btn(
        value='End',
        type='submit',
        extra_classes='btn-primary',
        form='endDeliveryForm'
    )

    return bootstrap.modal(
        id='endDeliveryModal',
        label='endDeliveryLable',
        title='End Delivery',
        body_content=form,
        footer_content=end_button
    )


def end_shift_modal(shift, csrf_token):
    # fields
    # start time
    fields = bootstrap.field(
        label='Start time:',
        input_type='text',
        id='start_time',
        value=shift.start_time,
        required=True
    )
    # distance
    fields += bootstrap.field(
        label='Total Distance:',
        input_type='number',
        id='distance',
        step='any',
        min=0,
        required=True
    )
    # fuel economy
    fields += bootstrap.field(
        label='Fuel Economy:',
        input_type='number',
        id='fuel_economy',
        step='any',
        min=0,
        required=True
    )
    # recorded hours
    fields += bootstrap.field(
        label='Recorded Hours:',
        input_type='number',
        id='recorded_hours',
        step='any',
        min=0,
        required=True
    )
    # vehicle compensation
    fields += bootstrap.field(
        label='Vehicle Compensation:',
        input_type='number',
        id='vehicle_compensation',
        step='any',
        min=0,
        required=True
    )
    # device compensation
    fields += bootstrap.field(
        label='Device Compensation:',
        input_type='number',
        id='device_compensation',
        step='any',
        min=0,
        required=True
    )
    # extra tips claimed
    fields += bootstrap.field(
        label='Extra Tips Claimed:',
        input_type='number',
        id='extra_tips_claimed',
        value=0.0,
        step='any',
        min=0,
        required=True
    )

    # form
    form = base_form(
        content=fields,
        action=values.base_id_url.format(
            reverse(values.end_shift_view),
            values.shift_id,
            shift.pk
        ),
        id='endShiftForm',
        csrf_token=csrf_token
    )

    # add/submit button
    add_button = bootstrap.btn(
        value='Add',
        type='submit',
        extra_classes='btn-primary',
        form='endShiftForm'
    )

    return bootstrap.modal(
        id='endShiftModal',
        label='endShiftLable',
        title='End Shift',
        body_content=form,
        footer_content=add_button
    )


def end_split_modal(shift, csrf_token):
    if Split.objects.filter(shift=shift).count() == 1:
        split = Split.objects.get(shift=shift)

        # fields
        # start time
        fields = bootstrap.field(
            label='Start time:',
            input_type='text',
            id='start_time',
            value=split.start_time,
            required=True
        )
        # distance
        fields += bootstrap.field(
            label='Total Distance:',
            input_type='number',
            id='distance',
            step='any',
            min=0,
            required=True
        )

        # form
        form = base_form(
            content=fields,
            action=values.base_id_url.format(
                reverse(values.end_split_view),
                values.shift_id,
                shift.pk
            ),
            id='endSplitForm',
            csrf_token=csrf_token
        )

        # add/submit button
        add_button = bootstrap.btn(
            value='Add',
            type='submit',
            extra_classes='btn-primary',
            form='endSplitForm'
        )

        return bootstrap.modal(
            id='endSplitModal',
            label='endSplitLable',
            title='End Split',
            body_content=form,
            footer_content=add_button
        )
    
    return ''
