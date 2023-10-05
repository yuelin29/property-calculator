
def get_repayment(rate, nper, pv):
    return round(pv * rate * (1 + rate) ** nper / ((1 + rate) ** nper - 1), 2)


def get_pv(rate, nper, pmt):
    return pmt / rate*((1 + rate)**nper - 1) / (1 + rate)**nper
