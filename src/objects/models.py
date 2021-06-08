from django.db import models

class Shift(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    fuel_economy = models.FloatField(null=True, blank=True)
    recorded_hours = models.FloatField(null=True, blank=True)
    vehicle_compensation = models.FloatField(null=True, blank=True)
    device_compensation = models.FloatField(null=True, blank=True)
    extra_tips_claimed = models.FloatField(null=True, blank=True)
    daily_delivery_id = models.IntegerField(default=0)
    daily_extra_stop_id = models.IntegerField(default=0)
    daily_split_id = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.date}'


class Delivery(models.Model):
    shift = models.ForeignKey(
        to=Shift,
        on_delete=models.CASCADE
    )

    daily_id = models.IntegerField(default=0)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    average_speed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.shift.date}, Delivery: #{self.daily_id + 1}'


class Order(models.Model):
    delivery = models.ForeignKey(to=Delivery, on_delete=models.CASCADE)

    daily_id = models.IntegerField(default=0)
    end_time = models.TimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{}, Delivery #{}, Order: #{}'.format(
            self.delivery.shift.date,
            (self.delivery.daily_id + 1),
            self.daily_id
        )


class Tip(models.Model):
    order = models.ForeignKey(
            to=Order,
            on_delete=models.CASCADE,
            null=True, blank=True
        )
    shift = models.ForeignKey(
            to=Shift,
            on_delete=models.CASCADE,
            null=True, blank=True
        )

    card = models.FloatField(default=0.0, null=True, blank=True)
    cash = models.FloatField(default=0.0, null=True, blank=True)
    unknown = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        if self.shift is not None:
            return '{}, Tip: ${}'.format(
                self.shift.date,
                (self.card + self.cash + self.unknown)
            )
        elif self.order is not None:
            return '{}, Order #{} Tip: ${}'.format(
                self.order.delivery.shift.date,
                self.order.daily_id,
                (self.card + self.cash + self.unknown)
            )
    
    def collection(self):
        return [self.card, self.cash, self.unknown]


class ExtraStop(models.Model):
    delivery = models.ForeignKey(
            to=Delivery,
            on_delete=models.CASCADE,
            null=True, blank=True
        )
    shift = models.ForeignKey(
            to=Shift,
            on_delete=models.CASCADE,
            null=True, blank=True
        )

    location = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    distance = models.FloatField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    daily_id = models.IntegerField(default=0)


class Split(models.Model):
    shift = models.ForeignKey(to=Shift, on_delete=models.CASCADE)

    daily_id = models.IntegerField(default=0)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.shift.date}, split'
