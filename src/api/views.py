from django.shortcuts import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import JsonResponse

from api.serializers import\
    DeliverySerializer,\
    ExtraStopSerializer,\
    OrderSerializer,\
    ShiftSerializer,\
    SplitSerializer,\
    TipSerializer
from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip
from resources import keys
from resources.functions import delivery_json_unprep, extra_stop_json_unprep, order_json_unprep, shift_json_unprep, split_json_unprep


def send_completed_shift(request, *args, **kwargs):
    if request.method == 'GET':
        # shift
        shift = Shift.objects.get(pk=json.loads(request.body)['pk'])
        shift_data = ShiftSerializer(shift).data

        # deliveries
        if Delivery.objects.filter(shift_id=shift.pk).exists():
            shift_data['deliveries'] = []
            for delivery in Delivery.objects.filter(shift_id=shift.pk):
                delivery_data = DeliverySerializer(delivery).data

                # orders
                delivery_data['orders'] = []
                for order in Order.objects.filter(delivery_id=delivery.pk):
                    order_data = OrderSerializer(order).data

                    # tip
                    order_data['tip'] =\
                        TipSerializer(Tip.objects.get(order_id=order.pk)).data
                    
                    delivery_data['orders'].append(order_data)

                # extra stops
                if ExtraStop.objects.filter(delivery_id=delivery.pk).exists():
                    delivery_data['extra_stops'] = [
                        ExtraStopSerializer(extra_stop).data for extra_stop
                        in ExtraStop.objects.filter(delivery_id=delivery.pk)
                    ]

                shift_data['deliveries'].append(delivery_data)

        # shift extra stops
        if ExtraStop.objects.filter(shift_id=shift.pk).exists():
            shift_data['extra_stops'] = [
                ExtraStopSerializer(extra_stop).data for extra_stop
                in ExtraStop.objects.filter(shift_id=shift.pk)
            ]

        # carry out tips
        if Tip.objects.filter(shift_id=shift.pk).exists():
            shift_data['carry_out_tips'] = [
                TipSerializer(tip).data for tip
                in Tip.objects.filter(shift_id=shift.pk)
            ]

        # split
        if Split.objects.filter(shift_id=shift.pk).exists():
            shift_data['split'] =\
                SplitSerializer(Split.objects.get(shift_id=shift.pk)).data
        
        return JsonResponse(data=shift_data)
    
    else:
        return HttpResponse('')


@ensure_csrf_cookie
def receive_completed_shift(request, *args, **kwargs):

    if request.method == 'POST':
        # todo: stil need to construct json object containing pk's for response

        data = json.loads(request.body)
        # todo: need to convert back to date and times

        # remove deliveries data from shift dictionary
        deliveries_data = None
        if keys.deliveries in data.keys():
            deliveries_data = data.pop(keys.deliveries)

        # remove extra stop data from shift dictionary
        shift_extra_stops_data = None
        if keys.extra_stops in data.keys():
            shift_extra_stops_data = data.pop(keys.extra_stops)

        # remove carry out tips data from shift dictionary
        carry_out_tips_data = None
        if keys.carry_out_tips in data.keys():
            carry_out_tips_data = data.pop(keys.carry_out_tips)

        # remove split data from shift dictionary
        split_data = None
        if keys.split in data.keys():
            split_data = data.pop(keys.split)

        # shift
        serialized_shift = ShiftSerializer(data=shift_json_unprep(data))
        if serialized_shift.is_valid(raise_exception=True):
            shift = serialized_shift.save()

        # deliveries
        if deliveries_data is not None:
            for delivery_data in deliveries_data:

                # remove orders from delivery dictionary
                orders_data = None
                if keys.orders in delivery_data.keys():
                    orders_data = delivery_data.pop(keys.orders)

                # remove extra stops from delivery dictionary
                delivery_extra_stops_data = None
                if keys.extra_stops in delivery_data.keys():
                    delivery_extra_stops_data =\
                        delivery_data.pop(keys.extra_stops)

                delivery_data['shift'] = shift.pk
                serialized_delivery =\
                    DeliverySerializer(data=delivery_json_unprep(delivery_data))
                if serialized_delivery.is_valid(raise_exception=True):
                    delivery = serialized_delivery.save()

                # orders
                if orders_data is not None:
                    for order_data in orders_data:
                        tip_data = order_data.pop(keys.tip)

                        order_data['delivery'] = delivery.pk
                        serialized_order =\
                            OrderSerializer(data=order_json_unprep(order_data))
                        if serialized_order.is_valid(raise_exception=True):
                            order = serialized_order.save()

                        # tip
                        tip_data['order'] = order.pk
                        serialized_tip = TipSerializer(data=tip_data)
                        if serialized_tip.is_valid(raise_exception=True):
                            tip = serialized_tip.save()

                # delivery extra stops
                if delivery_extra_stops_data is not None:
                    for extra_stop_data in delivery_extra_stops_data:
                        extra_stop_data['delivery'] = delivery.pk
                        serialized_extra_stop = ExtraStopSerializer(
                            data=extra_stop_json_unprep(extra_stop_data)
                        )
                        if serialized_extra_stop.is_valid(raise_exception=True):
                            extra_stop = serialized_extra_stop.save()

        # shift extra stops
        if shift_extra_stops_data is not None:
            for extra_stop_data in shift_extra_stops_data:
                extra_stop_data['shift'] = shift.pk
                serialized_extra_stop = ExtraStopSerializer(
                    data=extra_stop_json_unprep(extra_stop_data)
                )
                if serialized_extra_stop.is_valid(raise_exception=True):
                    extra_stop = serialized_extra_stop.save()

        # carry out tips
        if carry_out_tips_data is not None:
            for tip_data in carry_out_tips_data:
                tip_data['shift'] =  shift.pk
                serialized_tip = TipSerializer(data=tip_data)
                if serialized_tip.is_valid(raise_exception=True):
                    tip = serialized_tip.save()

        # split
        if split_data is not None:
            split_data['shift'] = shift.pk
            serialized_split =\
                SplitSerializer(data=split_json_unprep(split_data))
            if serialized_split.is_valid(raise_exception=True):
                split = serialized_split.save()
        

        print(f'Shift for date, {shift.date}, has been uploaded.\n')
        return HttpResponse('')
    

    else:
        return HttpResponse('')


def receive_carry_out_tips(request, *args, **kwargs):
    data = json.loads(request.body)

    carry_out_tips_pk = {}
    for tip_key in data.keys():
        tip = Tip.objects.create(
            shift_id=data['shift_pk'],
            card=data['card'],
            cash=data['cash'],
            unknown=data['unknown']
        )
        carry_out_tips_pk[tip_key] = tip.pk

    return JsonResponse(carry_out_tips_pk)


def receive_delivery(request, *args, **kwargs):
    data = json.loads(request.body)

    delivery = Delivery.objects.create(
        shift_id=data['shift_pk'],
        start_time=To_Datetime(data['start_time']).from_datetime().time(),
        end_time=To_Datetime(data['end_time']).from_datetime().time(),
        distance=data['distance'],
        average_speed=data['average_speed'],
    )

    return JsonResponse({'delivery_pk': delivery.pk})


def receive_extra_stop(request, *args, **kwargs):
    data = json.loads(request.body)

    if 'shift_pk' in data.keys():
        extra_stop = ExtraStop.objects.create(
            shift_id=data['shift_pk'],
            start_time=To_Datetime(data['start_time']).from_datetime().time(),
            end_time=To_Datetime(data['end_time']).from_datetime().time(),
            distance=data['distance'],
            average_speed=data['average_speed'],
        )
        return JsonResponse({'extra_stop_pk': extra_stop.pk})

    elif 'delivery_pk' in data.keys():
        extra_stop = ExtraStop.objects.create(
            shift_id=data['shift_pk'],
            end_time=To_Datetime(data['end_time']).from_datetime().time(),
            distance=data['distance'],
            average_speed=data['average_speed'],
        )
        return JsonResponse({'extra_stop_pk': extra_stop.pk})


def receive_order(request, *args, **kwargs):
    data = json.loads(request.body)

    order = Order.objects.create(
        delivery_id=data['delivery_pk'],
        end_time=To_Datetime(data['end_time']).from_datetime().time(),
        distance=data['distance']
    )

    tip = Tip.objects.create(
        order_id=order.pk,
        card=data['card'],
        cash=data['cash'],
        unknown=data['unknown']
    )

    return JsonResponse({'order_pk': order.pk})


def receive_shift(request, *args, **kwargs):
    data = json.loads(request.body)

    shift = Shift.objects.create(
        date=To_Datetime(data['date']).from_datetime().date(),
        start_time=To_Datetime(data['start_time']).from_datetime().date(),
        end_time=To_Datetime(data['end_time']).from_datetime().date(),
        distance=data['distance'],
        fuel_economy=data['fuel_economy'],
        recorded_hours=data['recorded_hours'],
        vehicle_compensation=data['vehicle_compensation'],
        device_compensation=data['device_compensation'],
        extra_tips_claimed=data['extra_tips_claimed'],
    )

    return JsonResponse({'shift_pk': shift.pk})


def receive_split(request, *args, **kwargs):
    data = json.loads(request.body)

    split = Split.objects.create(
        shift_id=data['shift_pk'],
        start_time=To_Datetime(data['start_time']).from_datetime().time(),
        end_time=To_Datetime(data['end_time']).from_datetime().time(),
        distance=data['distance']
    )

    return JsonResponse({'split_pk': split.pk})
