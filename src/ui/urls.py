from django.urls import path

import resources.values as values
import ui.views as view

urlpatterns = [
     # add carry_out_tip
     path(route='add_carry_out_tip/',
          view=view.add_carry_out_tip,
          name=values.add_carry_out_tip_view
     ),
     # add order
     path(route='add_order/',
          view=view.add_order,
          name=values.add_order_view
     ),
     # add extra stop
     path(route='add_extra_stop/',
          view=view.add_extra_stop,
          name=values.add_extra_stop_view
     ),
     # delivery menu
     path(route='delivery_menu/',
          view=view.delivery_menu,
          name=values.delivery_menu_view
     ),
     # edit carry out tip
     path(route='edit_carry_out_tip/',
          view=view.edit_carry_out_tip,
          name=values.edit_carry_out_tip_view
     ),
     # edit delivery
     path(route='edit_delivery/',
          view=view.edit_delivery,
          name=values.edit_delivery_view
     ),
     # edit extra stop
     path(route='edit_extra_stop/',
          view=view.edit_extra_stop,
          name=values.edit_extra_stop_view
     ),
     # edit order
     path(route='edit_order/',
          view=view.edit_order,
          name=values.edit_order_view
     ),
     # edit split
     path(route='edit_split/',
          view=view.edit_split,
          name=values.edit_split_view
     ),
     # end delivery
     path(route='end_delivery/',
          view=view.end_delivery,
          name=values.end_delivery_view
     ),
     # end shift
     path(route='end_shift/',
          view=view.end_shift,
          name=values.end_shift_view
     ),
     # end split
     path(route='end_split/',
          view=view.end_split,
          name=values.end_split_view
     ),
     # main menu
     path(route='',
          view=view.main_menu,
          name=values.main_menu_view
     ),
     # shift menu
     path(route='shift_menu/',
          view=view.shift_menu,
          name=values.shift_menu_view
     ),
      # start delivery
     path(route='start_delivery/',
          view=view.start_delivery,
          name=values.start_delivery_view
     ),
      # start extra stop
     path(route='start_extra_stop/',
          view=view.start_extra_stop,
          name=values.start_extra_stop_view
     ),
     # start shift
     path(route='start_shift/',
          view=view.start_shift,
          name=values.start_shift_view
     ),
     # start split
     path(route='start_split/',
          view=view.start_split,
          name=values.start_split_view
     ),
]
