import math


AVD_RATE = [
    (3000000, (100, 0)),
    (3528240, (100, 0.1)),
    (4500000, (0, 0.015)),
    (4935480, (67500, 0.1)),
    (6000000, (0, 0.0225)),
    (6642860, (135000, 0.1)),
    (9000000, (0, 0.03)),
    (10080000, (270000, 0.1)),
    (20000000, (0, 0.0375)),
    (21739120, (750000, 0.1)),
    (21739121, (0, 0.0425)),
]  # price upper limit, (absolute amount, tax rate on excess amount from previous price upper limit)


def get_avd(**kwargs):
    '''
        return Ad Valorem Stamp Duty (AVD) tax amount
        tax rate refer to AVD_RATE
        tax amount returned should round up to the nearest integer
    '''
    property_price = kwargs['property_price']
    is_first_property = kwargs['is_first_property']
    is_pr = kwargs['is_pr']
    if is_first_property and is_pr:
        upper_limit_i = next((i for i, x in enumerate(AVD_RATE) if property_price <= x[0]), len(AVD_RATE)-1)
        if upper_limit_i % 2 == 1:
            return math.ceil((AVD_RATE[upper_limit_i][1][0] + AVD_RATE[upper_limit_i][1][1] * (property_price - AVD_RATE[upper_limit_i-1][0])))
        else:
            return math.ceil(property_price * AVD_RATE[upper_limit_i][1][1] + AVD_RATE[upper_limit_i][1][0])
    else:
        return math.ceil(property_price * 0.15)


def get_bsd(**kwargs):
    '''
        return Buyer's Stamp Duty (BSD) tax amount
        tax amount returned should round up to the nearest integer
    '''
    property_price = kwargs['property_price']
    is_pr = kwargs['is_pr']
    if is_pr:
        return 0
    else:
        return math.ceil(property_price * 0.15)


get_avd(property_price=3000000, is_first_property=True, is_pr=True)
get_avd(property_price=3000000, is_first_property=True, is_pr=False)
get_avd(property_price=3000000, is_first_property=False, is_pr=True)
get_avd(property_price=3000000, is_first_property=False, is_pr=False)

get_avd(property_price=3500000, is_first_property=True, is_pr=True)
get_avd(property_price=4500000, is_first_property=True, is_pr=True)
get_avd(property_price=5000000, is_first_property=True, is_pr=True)
get_avd(property_price=6500000, is_first_property=True, is_pr=True)
get_avd(property_price=9000000, is_first_property=True, is_pr=True)
get_avd(property_price=75000000, is_first_property=True, is_pr=True)

get_bsd(property_price=3000000, is_pr=True)
get_bsd(property_price=3500000, is_pr=True)
get_bsd(property_price=4500000, is_pr=True)
get_bsd(property_price=5000000, is_pr=True)
get_bsd(property_price=6500000, is_pr=True)
get_bsd(property_price=9000000, is_pr=True)
get_bsd(property_price=75000000, is_pr=True)
