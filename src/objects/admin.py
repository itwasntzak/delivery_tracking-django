from django.contrib import admin

from objects.models import Delivery, ExtraStop, Order, Shift, Split, Tip


class DeliveryInline(admin.TabularInline):
    model = Delivery
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class ExtraStopInline(admin.TabularInline):
    model = ExtraStop
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class OrderInline(admin.TabularInline):
    model = Order
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class SplitInline(admin.TabularInline):
    model = Split
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class TipInline(admin.TabularInline):
    model = Tip
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class ShiftAdmin(admin.ModelAdmin):
    inlines = [
        DeliveryInline,
        ExtraStopInline,
        TipInline,
        SplitInline
    ]


class DeliveryAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
        ExtraStopInline,
    ]


class DeliveryAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
        ExtraStopInline,
    ]


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        TipInline
    ]


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(ExtraStop)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Split)
admin.site.register(Tip)
