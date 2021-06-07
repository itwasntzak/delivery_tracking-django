from datetime import datetime

from django.shortcuts import redirect, render
from django.urls import reverse
from objects.models import Delivery, ExtraStop, Shift, Order, Split, Tip
import objects.forms as forms

import py_web_ui.bootstrap as bootstrap
import resources.values as values
import ui.elements.buttons as buttons
import ui.elements.fields as fields
import ui.elements.forms as html_forms
import ui.elements.layout as layout
import ui.elements.composite as composite


# menus/ui
def delivery_menu(request):
    # todo: need to fix this to work with all the new changes

    # todo: have delivery details diplay below buttons
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a warning if a order hasnt been added but end delivery is pressed

    delivery = Delivery.objects.get(pk=request.GET.get(values.delivery_id))

    # logo bar
    body_html = [ composite.logo_bar() ]
    # title text
    body_html.append(
        composite.title_text('Delivery Menu:', 'What would you like to do?')
    )

    # buttons
    body_html.append(layout.three_button_row(
        # order button 
        composite.add_order_button_modal(delivery, request),
        # extra stop button
        composite.add_extra_stop_button_modal(delivery, request),
        # end delivery
        composite.end_delivery_button_modal(delivery, request)
    ))

    # order buttons
    body_html.append(
        composite.edit_orders_button_modal_group(delivery, request)
    )
    # extra stops buttons
    body_html.append(
        composite.edit_extra_stops_button_modal_group(delivery, request)
    )

    context = {
        'body_html': bootstrap.container('\n'.join(body_html), fluid=True),
    }

    return render(request, 'index.html', context)


def main_menu(request):
    # todo: work on turn this menu into more of a dashboard

    # logo bar
    body_html = [ composite.logo_bar() ]
    # title text
    body_html.append(
        composite.title_text('Welcome!', 'What would you like to do?')
    )
    # buttons
    body_html.append(layout.three_button_row(
        # order button 
        buttons.shift(),
        # extra stop button
        buttons.view_shifts(),
        # end delivery
        buttons.view_statistics()
    ))
    # container
    context = {
        'body_html': bootstrap.container('\n'.join(body_html), fluid=True)
    }

    return render(request, 'index.html', context)


def shift_menu(request):
    # todo: have shift details displayed at bottom of shift menu
    # todo: make a modal pop up or a toast apear notifying extra stop was started
    # todo: disable other ui buttons a split or extra stop is in progress
    # todo: add a check that raises an error if an id isnt included in GET

    # get shift
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    # logo bar
    body_html = [ composite.logo_bar() ]
    # title text
    body_html.append(composite.title_text('Shift Menu:', 'What would you like to do?'))

    # todo: need to add the modals for the control buttons
    # buttons
    # top control buttons
    body_html.append(layout.three_button_row(
        # delivery button
        buttons.start_delivery(shift),
        # extra stop button
        composite.add_extra_stop_button_modal(shift, request),
        # carry out tip button
        composite.add_carry_out_tip_button_modal(shift, request)
    ))
    # bottom control buttons
    body_html.append(layout.two_button_row(
        # split button
        # todo: add conditional so remove split button if split is completed
        composite.split_button_modal(shift, request),
        # end shift button
        composite.end_shift_button_modal(shift, request)
    ))

    # todo: trying to skip having a row and col for the layout, might brake
    # edit deliveries group
    body_html.append(
        composite.edit_deliveries_button_modal_group(shift, request)
    )
    # edit carry out tips group
    body_html.append(
        composite.edit_carry_out_tips_button_modal_group(shift, request)
    )
    # edit orders group
    body_html.append(composite.edit_orders_button_modal_group(shift, request))
    # edit extra stops group
    body_html.append(
        composite.edit_extra_stops_button_modal_group(shift, request)
    )
    # edit split group
    body_html.append(composite.edit_split_button_modal_group(shift, request))

    # container
    context = {
        'body_html': bootstrap.container('\n'.join(body_html), fluid=True)
    }

    return render(request, 'index.html', context)


# functional/ux
def add_carry_out_tip(request):
    # todo: add a check that raises an error if an id isnt included in GET

    if request.method == 'POST':
        shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

        form = forms.TipForm(request.POST)
        if form.is_valid():
            tip = Tip.objects.create(
                shift=shift,
                card=request.POST.get(values.card_field_id),
                cash=request.POST.get(values.cash_field_id)
            )
        else:
            print(form.errors)

        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                shift.pk
            )
        )


def add_order(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    
    if request.method == 'POST':
        delivery_id = request.GET.get(values.delivery_id)
        delivery = Delivery.objects.get(pk=delivery_id)

        order_form = forms.OrderForm(request.POST)
        tip_form = forms.TipForm(request.POST)

        if order_form.is_valid():
            order = Order.objects.create(
                delivery=delivery,
                end_time=now.time(),
                daily_id=request.POST.get(values.daily_id_field_id),
                distance=request.POST.get(values.distance_field_id)
            )
        else:
            print(order_form.errors)

        if tip_form.is_valid():
            tip = Tip.objects.create(
                order=order,
                card=request.POST.get(values.card_field_id),
                cash=request.POST.get(values.cash_field_id)
            )
        else:
            print(tip_form.errors)
        
        return redirect(values.base_id_url.format(
            reverse(values.delivery_menu_view),
            values.delivery_id,
            delivery_id
        ))


def add_extra_stop(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()

    if request.method == 'POST':
        location = request.POST.get(values.location_field_id)
        reason = request.POST.get(values.reason_field_id)
        distance = request.POST.get(values.distance_field_id)
        note = request.POST.get(values.note_field_id)

        # shift
        if values.shift_id in request.GET:
            shift = Shift.objects.get(pk=request.GET.get(values.shift_id))


            for extra_stop in ExtraStop.objects.filter(shift=shift):
                # extra stop in progress
                if extra_stop.end_time is None:
                    form = forms.ExtraStopForm(request.POST)

                    if form.is_valid():
                        # todo: this currently doesnt work
                        extra_stop.start_time =\
                            request.POST.get(values.start_time_field_id)
                        extra_stop.end_time = now.time()
                        extra_stop.location = location
                        extra_stop.reason = reason
                        extra_stop.distance = distance
                        extra_stop.save()
                        print('\n\nsuccess\n\n')
                    else:
                        print(form.errors)

                    break

            return redirect(values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                shift.id
            ))

        # delivery
        elif values.delivery_id in request.GET:
            delivery_id = request.GET.get(values.delivery_id)
            delivery = Delivery.objects.get(pk=delivery_id)

            form = forms.ExtraStopForm(request.POST)
            form.end_time = now.time()

            if form.is_valid():
                extra_stop = ExtraStop.objects.create(
                    delivery=delivery,
                    end_time=now.time(),
                    location=location,
                    reason=reason,
                    distance=distance,
                )
            else:
                print(form.errors)

            return redirect(values.base_id_url.format(
                reverse(values.delivery_menu_view),
                values.delivery_id,
                delivery_id
            ))


def edit_carry_out_tip(request):
    # todo: add a check that raises an error if an id isnt included in GET

    if request.method == 'POST':
        form = forms.TipForm(request.POST)
        if form.is_valid():
            tip = Tip.objects.get(pk=request.GET.get(values.tip_id))
            tip.card = request.POST.get(values.card_field_id)
            tip.cash = request.POST.get(values.cash_field_id)
            tip.save()
        else:
            print(form.errors)

        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                tip.shift.pk
            )
        )


def edit_delivery(request):
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a delete button incase the user want to delete an delivery
    # todo: need to conditinaly redirect back to the menu that called this

    if request.method == 'POST':
        delivery_id = request.GET.get(values.delivery_id)
        form = forms.EditDeliveryForm(request.POST)

        if form.is_valid():
            delivery = Delivery.objects.get(pk=delivery_id)
            delivery.start_time = request.POST.get(values.start_time_field_id)
            delivery.end_time = request.POST.get(values.end_time_field_id)
            delivery.distance = request.POST.get(values.distance_field_id)
            delivery.average_speed =\
                request.POST.get(values.average_speed_field_id)
            delivery.save()

            delivery.shift.daily_delivery_id += 1
            delivery.shift.save()
        else:
            print(form.errors)
        
        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                delivery.shift.pk
            )
        )


def edit_extra_stop(request):
    # todo: add a check that raises an error if an id isnt included in GET

    if request.method == 'POST':
        extra_stop = ExtraStop.objects.get(
            pk=request.GET.get(values.extra_stop_id)
        )
        end_time = request.POST.get(values.end_time_field_id)
        location = request.POST.get(values.location_field_id)
        reason = request.POST.get(values.reason_field_id)
        distance = request.POST.get(values.distance_field_id)

        form = forms.ExtraStopForm(request.POST)
        if form.is_valid():
            # shift
            if extra_stop.shift is not None:
                start_time = request.POST.get(values.start_time_field_id)
                extra_stop.start_time = start_time
                extra_stop.end_time = end_time
                extra_stop.location = location
                extra_stop.reason = reason
                extra_stop.distance = distance
                extra_stop.save()

                return redirect(values.base_id_url.format(
                    reverse(values.shift_menu_view),
                    values.shift_id,
                    extra_stop.shift.id
                    )
                )

            # delivery
            elif extra_stop.delivery is not None:
                extra_stop.end_time=end_time
                extra_stop.location=location
                extra_stop.reason=reason
                extra_stop.distance=distance
                extra_stop.save()

        else:
            print(form.errors)


        menu = request.POST.get(values.sending_menu_field_id)
        if menu == 'd':
            return redirect(values.base_id_url.format(
                reverse(values.delivery_menu_view),
                values.delivery_id,
                extra_stop.delivery.pk
                )
            )
        elif menu == 's':
            return redirect(values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                extra_stop.delivery.shift.pk
                )
            )


def edit_order(request):
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a delete button incase the user want to delete an order

    if request.method == 'POST':
        order_form = forms.EditOrderForm(request.POST)
        tip_form = forms.TipForm(request.POST)


        if order_form.is_valid():
            order = Order.objects.get(pk=request.GET.get(values.order_id))
            print(order.daily_id)
            order.daily_id = request.POST.get(values.daily_id_field_id)
            order.end_time = request.POST.get(values.end_time_field_id)
            order.distance = request.POST.get(values.distance_field_id)
            order.save()
            print(order.daily_id)

            if tip_form.is_valid():
                tip = Tip.objects.get(order=order)
                tip.card = request.POST.get(values.card_field_id)
                tip.cash = request.POST.get(values.cash_field_id)
                tip.save()

            else:
                print(tip_form.errors)
        else:
            print(order_form.errors)

        
        sending_menu = request.POST.get(values.sending_menu_field_id)
        if sending_menu == 's':
            return redirect(
                values.base_id_url.format(
                    reverse(values.shift_menu_view),
                    values.shift_id,
                    order.delivery.shift.pk
                )
            )

        elif sending_menu == 'd':        
            return redirect(
                values.base_id_url.format(
                    reverse(values.delivery_menu_view),
                    values.delivery_id,
                    order.delivery.pk
                )
            )


def edit_split(request):
    split = Split.objects.get(pk=request.GET.get(values.split_id))

    form = forms.EditSplitForm(request.POST)
    if form.is_valid():
        split.start_time = request.POST.get(values.start_time_field_id)
        split.end_time = request.POST.get(values.end_time_field_id)
        split.distance = request.POST.get(values.distance_field_id)
        split.note = request.POST.get(values.note_field_id)
        split.save()
    else:
        print(form.errors)

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            split.shift.pk
        )
    )


def end_delivery(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()

    if request.method == 'POST':
        delivery_id = request.GET.get(values.delivery_id)
        form = forms.AddDeliveryForm(request.POST)

        if form.is_valid():
            delivery = Delivery.objects.get(pk=delivery_id)
            delivery.distance = request.POST.get(values.distance_field_id)
            delivery.average_speed =\
                request.POST.get(values.average_speed_field_id)
            delivery.end_time = now.time()
            delivery.save()

            delivery.shift.daily_delivery_id += 1
            delivery.shift.save()
        else:
            print(form.errors)
        
        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                delivery.shift.pk
            )
        )


def end_shift(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()

    if request.method == 'POST':
        form = forms.ShiftForm(request.POST)

        if form.is_valid():
            shift = Shift.objects.get(pk=request.GET.get(values.shift_id))
            shift.start_time = request.POST.get(values.start_time_field_id)
            shift.distance = request.POST.get(values.distance_field_id)
            shift.fuel_economy = request.POST.get(values.fuel_economy_field_id)
            shift.recorded_hours =\
                request.POST.get(values.recorded_hours_field_id)
            shift.vehicle_compensation =\
                request.POST.get(values.vehicle_compensation_field_id)
            shift.device_compensation =\
                request.POST.get(values.device_compensation_field_id)
            shift.extra_tips_claimed =\
                request.POST.get(values.extra_tips_claimed_field_id)
            shift.end_time = now.time()
            shift.save()
        else:
            print(form.errors)
        
        return redirect(reverse(values.main_menu_view))


def end_split(request):
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: need to update to get the split pk from GET instead of shift pk

    now = datetime.now()
    split = Split.objects.get(pk=request.GET.get(values.split_id))

    if request.method == 'POST':
        form = forms.SplitForm(request.POST)
        if form.is_valid():
            split.start_time = request.POST.get(values.start_time_field_id)
            split.distance = request.POST.get(values.distance_field_id)
            split.end_time = now.time()
            split.note = request.POST.get(values.note_field_id)
            split.save()

            split.shift.daily_split_id += 1
            split.shift.save()
        else:
            print(form.errors)
        
        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                split.shift.pk
            )
        )


def start_delivery(request):
    # todo: make sure a new delivery cant be created if one isnt finished
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    delivery = Delivery.objects.create(
        shift=shift,
        start_time=now.time(),
        daily_id=shift.daily_delivery_id
    )

    return redirect(
        values.base_id_url.format(
           reverse(values.delivery_menu_view),
            values.delivery_id,
            delivery.pk
        )
    )


def start_extra_stop(request):
    # todo: make sure a new extra stop cant be created if one isnt finished
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    ExtraStop.objects.create(
        shift=shift,
        start_time=now.time()
    )

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            shift.pk
        )
    )


def start_shift(request):
    # todo: make sure a new shift cant be created if one isnt finished
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.create(
        date=now.date(),
        start_time=now.time()
    )

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            shift.pk
        )
    )


def start_split(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    Split.objects.create(
        shift=shift,
        start_time=now.time(),
        daily_id=shift.daily_split_id
    )

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            shift.pk
        )
    )
