from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip

import py_web_ui.bootstrap as bootstrap
import py_web_ui.html as html
import resources.values as values
import ui.elements.buttons as buttons
import ui.elements.fields as fields
import ui.elements.forms as forms
import ui.elements.layout as layout
import ui.elements.modals as modals


def add_carry_out_tip_button_modal(shift, request):
    return '\n'.join([
        buttons.add_carry_out_tip(),
        modals.add_carry_out_tip(
            forms.add_carry_out_tip(shift, fields.tip(), request),
            buttons.add(values.add_carry_out_tip_form_id.format(''))
        )
    ])


def add_extra_stop_button_modal(parent, request):
    parent_info = { 'id': parent.pk }
    extra_stop = None
    if isinstance(parent, Shift):
        parent_info['type'] = values.shift_id

        for extra_stop in ExtraStop.objects.filter(shift=parent):
            if extra_stop.start_time is not None:
                break
            else:
                extra_stop = None
    elif isinstance(parent, Delivery):
        parent_info['type'] = values.delivery_id

    return '\n'.join([
        buttons.extra_stop(parent),
        modals.add_extra_stop(
            forms.add_extra_stop(
                parent_info,
                fields.add_extra_stop(extra_stop),
                request
            ),
            buttons.add(values.add_extra_stop_form_id.format(''))
        )
    ])


def add_order_button_modal(delivery, request):
    return '\n'.join([
        buttons.add_order(),
        modals.add_order(
            forms.add_order(delivery, fields.add_order(), request),
            buttons.add(values.add_order_form_id)
        )
    ])


# todo: add limit of col length then start a new button modal group row
#       or make vertical groups, and put the button groups next to each other
def edit_carry_out_tips_button_modal_group(shift, request):

    button_list = []
    modal_list = []
    for tip in Tip.objects.filter(shift=shift):
        button_list.append(buttons.edit_carry_out_tip(tip))
        modal_list.append(modals.edit_carry_out_tip(
            tip,
            forms.edit_carry_out_tip(tip, fields.tip(tip), request),
            buttons.save(values.edit_carry_out_tip_form_id.format(tip.pk))
        ))

    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Carry Out Tips:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Carry Out Tip Buttons and Modals'
            ),
            modal_group='\n'.join(modal_list)
        )
        return layout.button_modal_group_row_col(button_modal_group)

    return ''


def edit_deliveries_button_modal_group(shift, request):

    button_list = []
    modal_list = []
    for delivery in Delivery.objects.filter(shift=shift):
        # delivery has been completed
        if delivery.start_time is not None and delivery.end_time is not None:
            button_list.append(buttons.edit_delivery(delivery))
            modal_list.append(modals.edit_delivery(
                delivery,
                forms.edit_delivery(
                    delivery,
                    fields.edit_delivery(delivery),
                    request
                ),
                buttons.save(values.edit_delivery_form_id.format(delivery.pk))
            ))

    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Deliveries:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Delivery Buttons and Modals'
            ),
            modal_group='\n'.join(modal_list)
        )
        return layout.button_modal_group_row_col(button_modal_group)
    
    return ''


def edit_extra_stops_button_modal_group(parent, request):
    # get extra stops
    # shift
    if isinstance(parent, Shift):
        # get shift extra stops
        extra_stop_list = ExtraStop.objects.filter(shift=parent)
        # get delivery extra stops
        for delivery in Delivery.objects.filter(shift=parent):
            delivery_list = ExtraStop.objects.filter(delivery=delivery)
            # if the delivery has any extra stops
            if delivery_list.count() > 0:
                extra_stop_list = extra_stop_list.union(delivery_list)
    # delivery
    elif isinstance(parent, Delivery):
        extra_stop_list = ExtraStop.objects.filter(delivery=parent)

    button_list = []
    modal_list = []
    for extra_stop in extra_stop_list:
        if extra_stop.end_time is not None:
            button_list.append(buttons.edit_extra_stop(extra_stop, request))
            modal_list.append(modals.edit_extra_stop(
                extra_stop,
                forms.edit_extra_stop(
                    extra_stop,
                    fields.edit_extra_stop(extra_stop, request),
                    request
                ),
                buttons.save(
                    values.edit_extra_stop_form_id.format(extra_stop.pk)
                )
            ))

    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Extra Stops:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Extra Stop Buttons and Modals'
            ),
            modal_group='\n'.join(modal_list)
        )
        return layout.button_modal_group_row_col(button_modal_group)
    
    return ''


def edit_orders_button_modal_group(parent, request):

    order_list = []
    if isinstance(parent, Shift):
        for delivery in Delivery.objects.filter(shift=parent):
            for order in Order.objects.filter(delivery=delivery):
                order_list.append(order)
    elif isinstance(parent, Delivery):
        for order in Order.objects.filter(delivery=parent):
            order_list.append(order)

    button_list = []
    modal_list = []
    for order in order_list:
        # order has been finished
        if order.end_time is not None:
            tip = Tip.objects.get(order=order)
            button_list.append(buttons.edit_order(order, request))
            modal_list.append(modals.edit_order(
                order,
                forms.edit_order(
                    order,
                    fields.edit_order(order, tip, request),
                    request
                ),
                buttons.save(values.edit_order_form_id.format(order.pk))
            ))
    
    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Orders:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Order Buttons and Modals'
            ),
            modal_group='\n'.join(modal_list)
        )
        return layout.button_modal_group_row_col(button_modal_group)
    
    return ''


def edit_shifts_button_group():
    button_list = []
    for shift in Shift.objects.all():
        button_list.append(buttons.edit_shift(shift))
    
    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Shifts:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Shift Buttons'
            ),
            modal_group=''
        )
        return layout.button_modal_group_row_col(button_modal_group)
    
    return '' 


def edit_split_button_modal_group(shift, request):

    button_list = []
    modal_list = []
    for split in Split.objects.filter(shift=shift):
        # split is completed
        if split.end_time is not None:
            button_list.append(buttons.edit_split(split))
            modal_list.append(
                modals.edit_split(
                    split,
                    forms.edit_split(
                        split,
                        fields.split(split, edit=True),
                        request
                    ),
                    buttons.save(values.edit_split_form_id.format(split.pk))
                )
            )

    if len(button_list) > 0:
        button_modal_group = values.button_modal_group_layout.format(
            header=html.h3('Splits:'),
            button_group=layout.button_group(
                button_list=button_list,
                label='Edit Split Buttons and Modals'
            ),
            modal_group='\n'.join(modal_list)
        )
        return layout.button_modal_group_row_col(button_modal_group)
    
    return ''


def end_delivery_button_modal(delivery, request):
    return '\n'.join([
        buttons.end_delivery(delivery),
        modals.end_delivery(
            delivery,
            forms.end_delivery(
                delivery,
                fields.end_delivery(delivery),
                request
            ),
            buttons.end(values.end_delivery_form_id)
        )
    ])


def end_shift_button_modal(shift, request):
    return '\n'.join([
        buttons.end_shift(),
        modals.end_shift(
            forms.end_shift(shift, fields.end_shift(shift), request),
            buttons.end(values.end_shift_form_id)
        )
    ])


def split_button_modal(shift, request):
    split = None
    if Split.objects.filter(shift=shift).count() > 0:
        for split in Split.objects.filter(shift=shift):
            # split has been started
            if split.end_time is None:
                break
            else:
                split = None

    return '\n'.join([
        buttons.split(shift, split),
        modals.end_split(
            forms.end_split(split, fields.split(split, end=True), request),
            buttons.end(values.end_split_form_id)
        )
    ])


def logo_bar(value='Delviery Tracker'):
    return bootstrap.row(bootstrap.col(
        content=html.div(
            content=html.h4(
                content=value,
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
