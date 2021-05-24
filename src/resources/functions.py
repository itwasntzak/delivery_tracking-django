from .utility import To_Datetime
from copy import deepcopy

# todo: need to add conditional checking for keys to avoid errors

def shift_json_unprep(shift_data):
    shift = deepcopy(shift_data)

    shift['date'] = To_Datetime(shift_data['date']).from_date().date()

    shift['start_time'] =\
        To_Datetime(shift_data['start_time']).from_time().time()        

    shift['end_time'] = To_Datetime(shift_data['end_time']).from_time().time()

    return shift


def delivery_json_unprep(delivery_data):
    delivery = deepcopy(delivery_data)
    delivery['start_time'] =\
        To_Datetime(delivery_data['start_time']).from_time().time()
    delivery['end_time'] =\
        To_Datetime(delivery_data['end_time']).from_time().time()

    return delivery


def order_json_unprep(order_data):
    order = deepcopy(order_data)
    order['end_time'] = To_Datetime(order_data['end_time']).from_time().time()
    return order


def extra_stop_json_unprep(extra_stop_data):
    extra_stop = deepcopy(extra_stop_data)

    if 'start_time' in extra_stop_data.keys():
        extra_stop['start_time'] =\
            To_Datetime(extra_stop_data['start_time']).from_time().time()

    extra_stop['end_time'] =\
        To_Datetime(extra_stop_data['end_time']).from_time().time()
    
    return extra_stop


def split_json_unprep(split_data):
    split = deepcopy(split_data)
    split['start_time'] =\
        To_Datetime(split_data['start_time']).from_time().time()
    split['end_time'] =\
        To_Datetime(split_data['end_time']).from_time().time()
    
    return split
