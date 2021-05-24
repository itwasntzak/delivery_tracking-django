from datetime import datetime

from django.middleware.csrf import get_token
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from objects.models import Delivery, ExtraStop, Shift, Order, Split, Tip
from objects.forms import AddDeliveryForm, EditDeliveryForm, EditOrderForm, ExtraStopForm, OrderForm, ShiftForm, SplitForm, TipForm

import py_web_ui.bootstrap as bootstrap
import ui.elements as elements
import resources.values as values


# menus/ui
def delivery_menu(request):
    # todo: have delivery details diplay below buttons
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a warning if a order hasnt been added but end delivery is pressed

    delivery_pk = request.GET.get('delivery_id')
    delivery = Delivery.objects.get(pk=delivery_pk)

    # logo bar
    body_html = elements.logo_bar()
    # title text
    body_html +=\
        elements.title_text('Delivery Menu:', 'What would you like to do?')

    # buttons
    body_html += elements.three_button_row(
        # order button 
        elements.add_order_button(),
        # extra stop button
        elements.extra_stop_button(delivery),
        # end delivery
        elements.end_delivery_button()
    )

    # order buttons
    body_html += bootstrap.row(
        bootstrap.col(
            elements.delivery_order_button_group(delivery, request)
        ),
        extra_classes='mx-5'
    )

    # todo: figure out how to process form data
    # add order modal
    body_html += elements.add_order_modal(
        delivery=delivery,
        csrf_token=get_token(request)
    )
    # add extra stop modal
    body_html += elements.add_extra_stop_modal(
        parent=delivery,
        csrf_token=get_token(request)
    )
    # end delivery modeal
    body_html += elements.end_delivery_modal(
        delivery=delivery,
        csrf_token=get_token(request)
    )

    # container
    body_html = bootstrap.container(body_html, fluid=True)

    context = {
        'body_html': body_html,
    }

    return render(request, 'index.html', context)


def main_menu(request):
    # todo: work on turn this menu into more of a dashboard

    # logo bar
    body_html = elements.logo_bar()
    # title text
    body_html += elements.title_text('Welcome!', 'What would you like to do?')
    # buttons
    body_html += elements.three_button_row(
        # order button 
        elements.shift_button(),
        # extra stop button
        elements.view_shifts_button(),
        # end delivery
        elements.view_statistics_button()
    )
    # container
    body_html = bootstrap.container(body_html, fluid=True)

    return render(request, 'index.html', { 'body_html': body_html })


def shift_menu(request):
    # todo: have shift details displayed at bottom of shift menu
    # todo: make a modal pop up or a toast apear notifying extra stop was started
    # todo: disable other ui buttons a split or extra stop is in progress
    # todo: add a check that raises an error if an id isnt included in GET

    # get shift object
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    # logo bar
    body_html = elements.logo_bar()
    # title text
    body_html += elements.title_text('Shift Menu:', 'What would you like to do?')

    # buttons
    # top row buttons
    body_html += elements.three_button_row(
        # delivery button
        elements.delivery_button(shift),
        # extra stop button
        elements.extra_stop_button(shift),
        # carry out tip button
        elements.carry_out_tip_button()
    )
    # bottom row buttons
    body_html += elements.two_button_row(
        # split button
        # todo: add conditional so remove split button if split is completed
        elements.split_button(shift),
        # end shift button
        elements.end_shift_button(),
    )

    # todo: add button groups conditionaly if there are any of those objects
    # deliveries buttons
    body_html += bootstrap.row(
        bootstrap.col(
            content=elements.delivery_button_group(
                shift=shift,
                request=request
            ),
            size=12
        ),
        extra_classes='mx-5 my-5'
    )
    # order buttons
    body_html += bootstrap.row(
        bootstrap.col(
            content=elements.shift_order_button_group(
                shift=shift,
                request=request
            ),
            size=12
        ),
        extra_classes='mx-5 my-5'
    )
    # extra stops buttons
    body_html += bootstrap.row(
        bootstrap.col(
            content=elements.extra_stop_button_group(
                parent=shift,
                request=request
            ),
            size=12
        ),
        extra_classes='mx-5 my-5'
    )

    # modals
    # add carry out tip modal
    body_html += elements.add_carry_out_tip_modal(
        shift=shift,
        csrf_token=get_token(request)
    )
    # add extra stop modal
    body_html += elements.add_extra_stop_modal(
        parent=shift,
        csrf_token=get_token(request)
    )
    # end shift modal
    body_html += elements.end_shift_modal(
        shift=shift,
        csrf_token=get_token(request)
    )
    # end split modal
    body_html += elements.end_split_modal(
        shift=shift,
        csrf_token=get_token(request)
    )

    # container
    body_html = bootstrap.container(body_html, fluid=True)

    return render(request, 'index.html', { 'body_html': body_html })


# functional/ux
def add_carry_out_tip(request):
    # todo: add a check that raises an error if an id isnt included in GET

    if request.method == 'POST':
        shift_id = request.GET.get(values.shift_id)
        shift = Shift.objects.get(pk=shift_id)

        form = TipForm(request.POST)
        if form.is_valid():
            tip = Tip.objects.create(
                shift=shift,
                card=request.POST.get('card'),
                cash=request.POST.get('cash')
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

        order_form = OrderForm(request.POST)
        tip_form = TipForm(request.POST)

        if order_form.is_valid():
            order = Order.objects.create(
                delivery=delivery,
                end_time=now.time(),
                daily_id=request.POST.get('daily_id'),
                distance=request.POST.get('distance')
            )
        else:
            print(order_form.errors)

        if tip_form.is_valid():
            tip = Tip.objects.create(
                order=order,
                card=request.POST.get('card'),
                cash=request.POST.get('cash')
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
        location = request.POST.get('location')
        reason = request.POST.get('reason')
        distance = request.POST.get('distance')

        # shift
        if values.shift_id in request.GET:
            print('\n\shift\n\n')

            shift = Shift.objects.get(pk=request.GET.get(values.shift_id))


            for extra_stop in ExtraStop.objects.filter(shift=shift):
                # extra stop in progress
                if extra_stop.end_time is None:
                    form = ExtraStopForm(request.POST)

                    if form.is_valid():
                        # todo: this currently doesnt work
                        extra_stop.start_time = request.POST.get('start_time')
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

            form = ExtraStopForm(request.POST)
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


def edit_delivery(request):
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a delete button incase the user want to delete an delivery
    # todo: need to conditinaly redirect back to the menu that called this

    if request.method == 'POST':
        delivery_id = request.GET.get(values.delivery_id)
        form = EditDeliveryForm(request.POST)

        if form.is_valid():
            delivery = Delivery.objects.get(pk=delivery_id)
            delivery.start_time = request.POST.get('start_time')
            delivery.end_time = request.POST.get('end_time')
            delivery.distance = request.POST.get('distance')
            delivery.average_speed = request.POST.get('average_speed')
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
        extra_stop =\
            ExtraStop.objects.get(pk=request.GET.get(values.extra_stop_id))
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        reason = request.POST.get('reason')
        distance = request.POST.get('distance')

        # shift
        if extra_stop.shift is not None:
            start_time = request.POST.get('start_time')

            form = ExtraStopForm(request.POST)
            if form.is_valid():
                extra_stop.start_time = start_time
                extra_stop.end_time = end_time
                extra_stop.location = location
                extra_stop.reason = reason
                extra_stop.distance = distance
                extra_stop.save()
            else:
                print(form.errors)

            return redirect(values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                extra_stop.shift.id
            ))

        # delivery
        elif extra_stop.delivery is not None:
            form = ExtraStopForm(request.POST)
            if form.is_valid():
                extra_stop.end_time=end_time,
                extra_stop.location=location,
                extra_stop.reason=reason,
                extra_stop.distance=distance,
                extra_stop.save()
            else:
                print(form.errors)

            return redirect(values.base_id_url.format(
                reverse(values.delivery_menu_view),
                values.delivery_id,
                extra_stop.delivery.pk
            ))


def edit_order(request):
    # todo: add a check that raises an error if an id isnt included in GET
    # todo: add a delete button incase the user want to delete an order

    if request.method == 'POST':
        order_form = EditOrderForm(request.POST)
        tip_form = TipForm(request.POST)


        if order_form.is_valid():
            order = Order.objects.get(pk=request.GET.get(values.order_id))
            print(order.daily_id)
            order.daily_id = request.POST.get('daily_id')
            order.end_time = request.POST.get('end_time')
            order.distance = request.POST.get('distance')
            order.save()
            print(order.daily_id)

            if tip_form.is_valid():
                tip = Tip.objects.get(order=order)
                tip.card = request.POST.get('card')
                tip.cash = request.POST.get('cash')
                tip.save()

            else:
                print(tip_form.errors)
        else:
            print(order_form.errors)

        
        sending_menu = request.POST.get('menu')
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


def end_delivery(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()

    if request.method == 'POST':
        delivery_id = request.GET.get(values.delivery_id)
        form = AddDeliveryForm(request.POST)

        if form.is_valid():
            delivery = Delivery.objects.get(pk=delivery_id)
            delivery.distance = request.POST.get('distance')
            delivery.average_speed = request.POST.get('average_speed')
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
        form = ShiftForm(request.POST)

        if form.is_valid():
            shift = Shift.objects.get(pk=request.GET.get(values.shift_id))
            shift.start_time = request.POST.get('start_time')
            shift.distance = request.POST.get('distance')
            shift.fuel_economy = request.POST.get('fuel_economy')
            shift.recorded_hours = request.POST.get('recorded_hours')
            shift.vehicle_compensation = request.POST.get('vehicle_compensation')
            shift.device_compensation = request.POST.get('device_compensation')
            shift.extra_tips_claimed = request.POST.get('extra_tips_claimed')
            shift.end_time = now.time()
            shift.save()
        else:
            print(form.errors)
        
        return redirect(reverse(values.main_menu_view))


def end_split(request):
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()

    if request.method == 'POST':
        shift = Shift.objects.get(pk=request.GET.get(values.shift_id))
        form = SplitForm(request.POST)

        if form.is_valid():
            split = Split.objects.get(shift=shift)
            split.start_time = request.POST.get('start_time')
            split.distance = request.POST.get('distance')
            split.end_time = now.time()
            split.save()
        else:
            print(form.errors)
        
        return redirect(
            values.base_id_url.format(
                reverse(values.shift_menu_view),
                values.shift_id,
                shift.pk
            )
        )


def start_delivery(request):
    # todo: make sure a new delivery cant be created if one isnt finished
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.get(pk=request.GET.get(values.shift_id))

    delivery = Delivery.objects.create(
        shift=shift,
        daily_id=shift.daily_delivery_id,
        start_time=now.time()
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
    shift_id = request.GET.get(values.shift_id)
    shift = Shift.objects.get(pk=shift_id)
    
    ExtraStop.objects.create(
        shift=shift,
        start_time=now.time()
    )

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            shift_id
        )
    )


def start_shift(request):
    # todo: make sure a new shift cant be created if one isnt finished
    # todo: add a check that raises an error if an id isnt included in GET

    now = datetime.now()
    shift = Shift.objects.create(date=now.date(), start_time=now.time())

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

    Split.objects.create(shift=shift, start_time=now.time())

    return redirect(
        values.base_id_url.format(
            reverse(values.shift_menu_view),
            values.shift_id,
            shift.pk
        )
    )
