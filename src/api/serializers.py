from rest_framework import serializers

from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip


class ExtraStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraStop
        fields = [
            'pk', 'shift', 'delivery', 'daily_id',
            'start_time', 'end_time',
            'location', 'reason', 'distance'
        ]


class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = [
            'pk', 'shift',
            'start_time', 'end_time',
            'distance'
        ]


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = [
            'pk', 'shift', 'order',
            'card', 'cash', 'unknown'
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pk', 'delivery', 'daily_id',
            'end_time', 'distance'
        ]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            'pk', 'shift', 'daily_id',
            'start_time', 'end_time',
            'distance', 'average_speed'
        ]


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = [
            'pk', 'date', 'start_time', 'end_time',
            'distance', 'fuel_economy', 'recorded_hours',
            'vehicle_compensation', 'device_compensation',
            'extra_tips_claimed'
        ]
