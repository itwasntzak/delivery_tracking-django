from django.db.models import fields
from django.forms import ModelForm

from py_web_ui.bootstrap import modal
from .models import Delivery, ExtraStop, Order, Shift, Split, Tip


class AddDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            'start_time',
            'distance',
            'average_speed'
        ]


class EditDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            'start_time',
            'end_time',
            'distance',
            'average_speed'
        ]


class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'daily_id',
            'end_time',
            'distance'
        ]


class ExtraStopForm(ModelForm):
    class Meta:
        model = ExtraStop
        fields = [
            'start_time',
            'location',
            'reason',
            'distance'
        ]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'daily_id',
            'distance'
        ]


class TipForm(ModelForm):
    class Meta:
        model = Tip
        fields = [
            'card',
            'cash'
        ]


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'start_time',
            'distance',
            'fuel_economy',
            'recorded_hours',
            'vehicle_compensation',
            'device_compensation',
            'extra_tips_claimed'
        ]


class SplitForm(ModelForm):
    class Meta:
        model = Split
        fields = [
            'start_time',
            'distance'
        ]
