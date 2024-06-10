from django.forms import ModelForm

from .models import Delivery, ExtraStop, Order, Shift, Split, Tip
import resources.values as values


class AddDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            values.start_time_field_id,
            values.distance_field_id,
            values.average_speed_field_id
        ]


class EditDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            values.start_time_field_id,
            values.end_time_field_id,
            values.distance_field_id,
            values.average_speed_field_id
        ]


class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            values.daily_id_field_id,
            values.end_time_field_id,
            values.distance_field_id
        ]


class EditSplitForm(ModelForm):
    class Meta:
        model = Split
        fields = [
            values.end_time_field_id,
            values.start_time_field_id,
            values.distance_field_id,
            values.note_field_id
        ]


class EndDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            values.start_time_field_id,
            values.end_time_field_id,
            values.distance_field_id,
            values.average_speed_field_id
        ]
        


class ExtraStopForm(ModelForm):
    class Meta:
        model = ExtraStop
        fields = [
            values.start_time_field_id,
            values.location_field_id,
            values.reason_field_id,
            values.distance_field_id
        ]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            values.daily_id_field_id,
            values.distance_field_id
        ]


class TipForm(ModelForm):
    class Meta:
        model = Tip
        fields = [
            values.card_field_id,
            values.cash_field_id
        ]


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            values.start_time_field_id,
            values.distance_field_id,
            values.fuel_economy_field_id,
            values.recorded_hours_field_id,
            values.vehicle_compensation_field_id,
            values.device_compensation_field_id,
            values.extra_tips_claimed_field_id
        ]


class SplitForm(ModelForm):
    class Meta:
        model = Split
        fields = [
            values.start_time_field_id,
            values.distance_field_id,
            values.note_field_id
        ]


class StartDeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = [
            values.start_time_field_id,
            values.daily_id_field_id
        ]
