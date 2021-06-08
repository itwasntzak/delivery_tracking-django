from .utility import To_Datetime
from copy import deepcopy
import resources.values as values

# todo: need to add conditional checking for keys to avoid errors

def shift_json_unprep(shift_data):
    shift = deepcopy(shift_data)

    # date
    shift['date'] = To_Datetime(shift_data['date']).from_date().date()
    # start time
    if values.start_time_field_id in shift_data:
        shift[values.start_time_field_id] = To_Datetime(
            shift_data[values.start_time_field_id]
        ).from_time().time()
    # end time
    if values.end_time_field_id in shift_data:
        shift[values.end_time_field_id] = To_Datetime(
            shift_data[values.end_time_field_id]
        ).from_time().time()

    return shift


def delivery_json_unprep(delivery_data):
    delivery = deepcopy(delivery_data)

    # start time
    if values.start_time_field_id in delivery_data:
        delivery[values.start_time_field_id] = To_Datetime(
            delivery_data[values.start_time_field_id]
        ).from_time().time()
    # end time
    if values.end_time_field_id in delivery_data:
        delivery[values.end_time_field_id] = To_Datetime(
            delivery_data[values.end_time_field_id]
        ).from_time().time()

    return delivery


def order_json_unprep(order_data):
    order = deepcopy(order_data)

    # end time
    if values.end_time_field_id in order_data:
        order[values.end_time_field_id] = To_Datetime(
            order_data[values.end_time_field_id]
        ).from_time().time()

    return order


def extra_stop_json_unprep(extra_stop_data):
    extra_stop = deepcopy(extra_stop_data)

    # start time
    # .keys()
    if values.start_time_field_id in extra_stop_data:
        extra_stop[values.start_time_field_id] = To_Datetime(
            extra_stop_data[values.start_time_field_id]
        ).from_time().time()
    # end time
    if values.end_time_field_id in extra_stop_data:
        extra_stop[values.end_time_field_id] = To_Datetime(
            extra_stop_data[values.end_time_field_id]
        ).from_time().time()
    
    return extra_stop


def split_json_unprep(split_data):
    split = deepcopy(split_data)

    # start time
    if values.start_time_field_id in split_data:
        split[values.start_time_field_id] = To_Datetime(
            split_data[values.start_time_field_id]
        ).from_time().time()
    # end time
    if values.end_time_field_id in split_data:
        split[values.end_time_field_id] = To_Datetime(
            split_data[values.end_time_field_id]
        ).from_time().time()
    
    return split
