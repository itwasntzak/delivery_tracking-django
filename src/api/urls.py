from django.conf.urls import url
from django.urls import path

from .views import\
    receive_carry_out_tips,\
    receive_delivery,\
    receive_extra_stop,\
    receive_order,\
    receive_shift,\
    receive_split,\
    receive_completed_shift, send_completed_shift
#     csrf_request,\


urlpatterns = [
#     # csrf request
#     path(route='',
#          view=csrf_request,
#          name='csrf-request'),


    # receive completed shift
    path(route='receive_completed_shift/',
         view=receive_completed_shift,
         name='api-receive-completed-shift'),
     # send completed shift
     path(route='send_completed_shift/',
          view=send_completed_shift,
          name='api-send-completed-shift'),

#     # receive delivery
#     path(route='receive_delivery/',
#          view=receive_delivery,
#          name='api-receive-delivery'),
#     # receive extra stop
#     path(route='receive_extra_stop/',
#          view=receive_extra_stop,
#          name='api-receive-extra_stop'),
#     # receive shift
#     path(route='receive_shift/',
#          view=receive_shift,
#          name='api-receive-shift'),
#     # receive order
#     path(route='receive_order/',
#          view=receive_order,
#          name='api-receive-order'),
#     # receive split
#     path(route='receive_split/',
#          view=receive_split,
#          name='api-receive-split'),
#     # receive carry out tips
#     path(route='receive_carry_out_tips/',
#          view=receive_carry_out_tips,
#          name='api-receive-carry_out_tips'),
]