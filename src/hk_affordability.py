from utils import get_pv, get_repayment


def get_maximum_loan(down_payment):
    if down_payment <= 1000000:
        maximum_loan = down_payment * 9
    elif down_payment <= 2250000:
        maximum_loan = 9000000
    elif down_payment <= 3000000:
        maximum_loan = down_payment / 0.2 * (1 - 0.2)
    elif down_payment <= 5150000:
        maximum_loan = 12000000
    elif down_payment <= 9000000:
        maximum_loan = down_payment / 0.3 * (1 - 0.3)
    elif down_payment <= 12000000:
        maximum_loan = 30000000 - down_payment
    elif down_payment <= 18000000:
        maximum_loan = 18000000
    else:
        maximum_loan = down_payment * 1
    return maximum_loan


def calculate_affordability(**kwargs):
    '''
    :param kwargs:
        monthly_income: int
        affordable_monthly_loan_amount: int
        down_payment: int
        interest_rate: float
        repayment_period_year: int, default 30
        repayment_period_month: int, default 0
    :return:
        affordable_property_value: int
        max_loan_amount: int
        monthly_repayment: decimal number, 2 decimal place
        debt_to_income_ratio: float
        pass_dti: boolean
        stress_test_monthly_repayment: decimal number, 2 decimal place
        stress_test_debt_to_income_ratio: float
        pass_stress_test: boolean
    '''
    monthly_income = kwargs['monthly_income']
    affordable_monthly_loan_amount = kwargs['affordable_monthly_loan_amount']
    down_payment = kwargs['down_payment']
    interest_rate = kwargs['interest_rate'] # unit %
    repayment_period_year = kwargs['repayment_period_year']
    repayment_period_month = kwargs['repayment_period_month']

    loan_amount = get_pv(
        rate=interest_rate / 12 / 100,
        nper=repayment_period_year * 12 + repayment_period_month,
        pmt=affordable_monthly_loan_amount
    )
    max_loan_amount_based_on_down_payment = get_maximum_loan(down_payment)
    max_loan_amount = int(min(loan_amount, max_loan_amount_based_on_down_payment))
    affordable_property_value = max_loan_amount + down_payment

    monthly_repayment = get_repayment(
        rate=interest_rate / 12 / 100,
        nper=repayment_period_year * 12 + repayment_period_month,
        pv=max_loan_amount
    )
    debt_to_income_ratio = monthly_repayment / monthly_income

    stress_test_monthly_repayment = get_repayment(
        rate=(interest_rate + 2) / 12 / 100,
        nper=repayment_period_year * 12 + repayment_period_month,
        pv=max_loan_amount,
    )
    stress_test_debt_to_income_ratio = stress_test_monthly_repayment / monthly_income

    pass_dti = debt_to_income_ratio <= 0.5
    pass_stress_test = stress_test_debt_to_income_ratio <= 0.6

    return {
        "affordable_property_value": affordable_property_value,  # integer
        "max_loan_amount": max_loan_amount,  # integer
        "monthly_repayment": monthly_repayment,  # decimal number, 2 decimal place
        "debt_to_income_ratio": debt_to_income_ratio,  # float
        "pass_dti": pass_dti,  # boolean
        "stress_test_monthly_repayment": stress_test_monthly_repayment,  # decimal number, 2 decimal place
        "stress_test_debt_to_income_ratio": stress_test_debt_to_income_ratio,  # float
        "pass_stress_test": pass_stress_test,  # boolean
    }


test_1 = {
    "monthly_income": 50000,
    "down_payment": 100000,
    "affordable_monthly_loan_amount": 23500,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_1))
# {'affordable_property_value': 1000000, 'max_loan_amount': 900000, 'monthly_repayment': 4104.46, 'debt_to_income_ratio': 0.0820892, 'pass_dti': True, 'stress_test_monthly_repayment': 5180.91, 'stress_test_debt_to_income_ratio': 0.1036182, 'pass_stress_test': True}

test_2 = {
    "monthly_income": 50000,
    "down_payment": 1000000,
    "affordable_monthly_loan_amount": 23500,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_2))
# {'affordable_property_value': 6152929, 'max_loan_amount': 5152929, 'monthly_repayment': 23500.0, 'debt_to_income_ratio': 0.47, 'pass_dti': True, 'stress_test_monthly_repayment': 29663.17, 'stress_test_debt_to_income_ratio': 0.5932634, 'pass_stress_test': True}

test_3 = {
    "monthly_income": 500000,
    "down_payment": 1000000,
    "affordable_monthly_loan_amount": 235000,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_3))
# {'affordable_property_value': 10000000, 'max_loan_amount': 9000000, 'monthly_repayment': 41044.62, 'debt_to_income_ratio': 0.08208924000000001, 'pass_dti': True, 'stress_test_monthly_repayment': 51809.08, 'stress_test_debt_to_income_ratio': 0.10361816, 'pass_stress_test': True}

test_4 = {
    "monthly_income": 800000,
    "down_payment": 1000000,
    "affordable_monthly_loan_amount": 37600,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_4))
# {'affordable_property_value': 9244686, 'max_loan_amount': 8244686, 'monthly_repayment': 37600.0, 'debt_to_income_ratio': 0.047, 'pass_dti': True, 'stress_test_monthly_repayment': 47461.06, 'stress_test_debt_to_income_ratio': 0.059326325, 'pass_stress_test': True}

test_5 = {
    "monthly_income": 800000,
    "down_payment": 1200000,
    "affordable_monthly_loan_amount": 376000,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_5))
# {'affordable_property_value': 10200000, 'max_loan_amount': 9000000, 'monthly_repayment': 41044.62, 'debt_to_income_ratio': 0.051305775000000005, 'pass_dti': True, 'stress_test_monthly_repayment': 51809.08, 'stress_test_debt_to_income_ratio': 0.06476135, 'pass_stress_test': True}

test_6 = {
    "monthly_income": 800000,
    "down_payment": 3000000,
    "affordable_monthly_loan_amount": 376000,
    "interest_rate": 3.625,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_6))
# {'affordable_property_value': 15000000, 'max_loan_amount': 12000000, 'monthly_repayment': 54726.16, 'debt_to_income_ratio': 0.0684077, 'pass_dti': True, 'stress_test_monthly_repayment': 69078.77, 'stress_test_debt_to_income_ratio': 0.0863484625, 'pass_stress_test': True}

test_7 = {
    "monthly_income": 300000,
    "down_payment": 5000000,
    "affordable_monthly_loan_amount": 150000,
    "interest_rate": 4.125,
    "repayment_period_year": 30,
    "repayment_period_month": 0,
}
print(calculate_affordability(**test_7))
# {'affordable_property_value': 17000000, 'max_loan_amount': 12000000, 'monthly_repayment': 58157.97, 'debt_to_income_ratio': 0.1938599, 'pass_dti': True, 'stress_test_monthly_repayment': 72913.26, 'stress_test_debt_to_income_ratio': 0.2430442, 'pass_stress_test': True}
