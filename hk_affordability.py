
def get_repayment(rate, nper, pv):
    return round(pv * rate * (1 + rate) ** nper / ((1 + rate) ** nper - 1), 2)


def cal_affordability(**kwargs):
    monthly_income = kwargs['monthly_income']
    other_monthly_payment = kwargs['other_monthly_payment']
    down_payment = kwargs['down_payment']
    loan_amount = kwargs['loan_amount']
    interest_rate = kwargs['interest_rate'] # unit %
    repayment_period = kwargs['repayment_period'] # unit year

    total_payment = loan_amount
    monthly_repayment = get_repayment(
        rate=interest_rate / 100 / 12,
        nper=repayment_period * 12,
        pv=loan_amount,
    )
    property_value = loan_amount + down_payment
    debt_to_income_ratio = monthly_repayment / (monthly_income - other_monthly_payment)

    stress_test_monthly_repayment = get_repayment(
        rate=(interest_rate + 2) / 100 / 12,
        nper=repayment_period * 12,
        pv=loan_amount,
    )
    stress_test_debt_to_income_ratio = stress_test_monthly_repayment / (monthly_income - other_monthly_payment)
    pass_dti = debt_to_income_ratio <= 0.5
    pass_stress_test = stress_test_debt_to_income_ratio <= 0.6

    return {
        "total_payment": total_payment,
        "monthly_repayment": monthly_repayment,
        "property_value": property_value,
        "debt_to_income_ratio": debt_to_income_ratio,
        "pass_dti": pass_dti,
        "stress_test_debt_to_income_ratio": stress_test_debt_to_income_ratio,
        "pass_stress_test": pass_stress_test,
    }


test_1 = {
    "monthly_income": 40000,
    "other_monthly_payment": 0,
    "down_payment": 1600000,
    "loan_amount": 14400000,
    "interest_rate": 4,
    "repayment_period": 30,
}
print(cal_affordability(**test_1))
