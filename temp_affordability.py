import math
import numpy as np


def get_iwaa(age_list, income_list):
    iwaa = sum(np.array(age_list) * np.array(income_list)) / sum(income_list)
    return math.ceil(iwaa)


def get_max_loan_tenure(iwwa, property_type):
    if property_type == 'HDB':
        max_tenure = 25
    else:
        max_tenure = 30
    return min(max_tenure, 65 - iwwa)


def get_ltv_ratio(property_loan_count_list):
    effective_property_loan_count = max(property_loan_count_list)
    ltv_dict = {
        0: 75,
        1: 45,
        2: 35,
    } # key: property_loan_count, value: loan-to-value ratio
    property_loan_count = min(effective_property_loan_count, 2)
    return ltv_dict[property_loan_count]


def get_income_assessment_output(**kwargs):
    monthly_fixed_income = math.floor(kwargs['annualFixedIncome'] / 12)
    monthly_variable_income = math.floor(kwargs['annualVariableIncome'] / 12 * 0.7)
    monthly_rental_income = math.floor(kwargs['annualRentalIncome'] / 12 * 0.7)
    monthly_pledged_sgd_deposit = math.floor(kwargs['pledgedDeposit'] / 48)
    monthly_unpledged_sgd_deposit = math.floor(kwargs['unpledgedDeposit'] / 48 * 0.3)

    income_subtotal = monthly_fixed_income + monthly_variable_income + monthly_rental_income + monthly_pledged_sgd_deposit + monthly_unpledged_sgd_deposit
    income_used_for_calculation = math.floor(income_subtotal/10) * 10
    return {
        "incomeSubtotal": income_subtotal,
        "incomeUsedForCalculation": income_used_for_calculation
    }


def get_bsd(price):
    bsd_table = (
        (180000, 0.01),
        (180000, 0.02),
        (640000, 0.03),
        (500000, 0.04),
        (1500000, 0.05),
        # (infinity, 0.06),
    )
    tax = 0
    for price_tier, rate in bsd_table:
        tax_temp = rate * min(price_tier, price)
        temp_price = price - price_tier

        tax = tax + tax_temp
        if temp_price < 0:
            return tax
        else:
            price = temp_price
    tax_temp = 0.06 * price
    tax = tax + tax_temp
    return tax


def get_absd(borrowers, property_price):
    absd_table = {
        "Singaporean": [0, 0.17, 0.25],
        "SPR": [0.05, 0.25, 0.3],
        "Foreigner": [0.3, 0.3, 0.3],
    }
    nationality_list = [b['nationality'] for b in borrowers]
    existing_property_count_list = [b['existingPropertyCount'] for b in borrowers]
    absd_rate = 0
    for i in range(len(nationality_list)):
        nationality = nationality_list[i]
        existing_property_count = existing_property_count_list[i]
        existing_property_count_index = min(existing_property_count, 2)
        absd_rate_temp = absd_table[nationality][existing_property_count_index]
        absd_rate = max(absd_rate_temp, absd_rate)
    absd_amount = absd_rate * property_price
    return absd_rate, absd_amount


def get_pv(rate, nper, pmt):
    return pmt / rate*((1 + rate)**nper - 1) / (1 + rate)**nper


def get_mandatory_cash(borrowers, property_price):
    existing_property_loans_list = [b['numberOfExistingPropertyLoans'] for b in borrowers]
    effective_property_loans = max(existing_property_loans_list)

    if effective_property_loans > 0:
        cash_rate = 0.25
    else:
        cash_rate = 0.05
    cash_amount = property_price * cash_rate
    return cash_rate, cash_amount


def get_debt_assessment_output(**kwargs):
    monthly_property_loan_instalment = math.ceil(kwargs['monthlyPropertyLoanInstalment'])
    monthly_car_loan = math.ceil(kwargs['monthlyCarLoan'])
    monthly_unsecured_credit_card = math.ceil(kwargs['monthlyUnsecuredCredit'])
    monthly_secured_revolving_debt = math.ceil(kwargs['monthlySecuredRevolvingDebt'])
    guarantor_debt = math.ceil(kwargs['guarantorDebt'])

    debt_subtotal = monthly_property_loan_instalment + monthly_car_loan + monthly_unsecured_credit_card + monthly_secured_revolving_debt + guarantor_debt
    debt_used_for_calculation = math.ceil(debt_subtotal/10) * 10
    return {
        "debtSubtotal": debt_subtotal,
        "debtUsedForCalculation": debt_used_for_calculation
    }


def get_financial_position_summary_output(**kwargs):
    property_type = kwargs['propertyType'] # 'HDB', 'private', 'EC'
    borrowers = kwargs['borrowers']
    age_list = [b['age'] for b in borrowers]
    income_list = [b['incomeUsedForCalculation'] for b in borrowers]
    debt_list = [b['debtUsedForCalculation'] for b in borrowers]
    property_loan_count_list = [b['numberOfExistingPropertyLoans'] for b in borrowers]
    iwaa = get_iwaa(age_list, income_list)

    max_loan_tenure = get_max_loan_tenure(iwaa, property_type)

    total_income_of_borrowers = sum(income_list)
    total_debt_of_borrowers = sum(debt_list)

    msr_ceiling = total_income_of_borrowers * 0.3
    tdsr_ceiling = math.floor(total_income_of_borrowers * 0.55 / 1)

    max_ltv_ratio = get_ltv_ratio(property_loan_count_list) if property_type == 'private' else 75

    amount_available_for_property_loan_instalment = max(tdsr_ceiling - total_debt_of_borrowers, 0) if property_type == 'private' else msr_ceiling

    return {
        "iwaa": iwaa,
        "maxLoanTenure": max_loan_tenure,
        "totalIncomeOfBorrowers": total_income_of_borrowers,
        "msrCeiling": msr_ceiling,
        "tdsrCeiling": tdsr_ceiling,
        "maxLtvRatio": max_ltv_ratio,
        "totalDebtOfBorrowers": total_debt_of_borrowers,
        "amountAvailableForPropertyLoanInstalment": amount_available_for_property_loan_instalment,
    }


def get_loan_and_property_options_summary_output(**kwargs):
    loan_tenure = kwargs['loanTenure']
    payment_ceiling = kwargs['amountAvailableForPropertyLoanInstalment']
    ltv_ratio = kwargs['ltvRatio']
    medium_term_interest_rate = kwargs['mediumTermInterestRate']
    max_property_loan_amount_raw = get_pv(
        rate=medium_term_interest_rate / 12 / 100,
        nper=loan_tenure * 12,
        pmt=payment_ceiling,
    )
    max_property_loan_amount = math.floor(max_property_loan_amount_raw / 1000) * 1000
    highest_property_price_raw = max_property_loan_amount / ltv_ratio * 100
    highest_property_price = math.floor(highest_property_price_raw / 1000) * 1000

    mandatory_cash = get_mandatory_cash(kwargs["borrowers"], highest_property_price)
    cpf_oa = 0.2, highest_property_price * 0.2
    bsd = get_bsd(highest_property_price)
    absd = get_absd(kwargs["borrowers"], highest_property_price)

    return {
        "maxPropertyLoanAmount": max_property_loan_amount,
        "highestAffordablePrice": highest_property_price,
        "mandatoryCash": mandatory_cash,
        "cpfOrdinaryAccount": cpf_oa,
        "bsd": bsd,
        "additonalBsd": absd,
    }


property_type_input = "private" # private, EC, HDB

income_assessment_input = {
    "annualFixedIncome": 52000, # monthlyFixedIncome derived from annualFixedIncome
    "annualVariableIncome": 8000, # monthlyVariableIncome derived from annualVariableIncome
    "annualRentalIncome": 0,
    "pledgedDeposit": 50000,
    "unpledgedDeposit": 50000
}


income_assessment_input_2 = {
    "annualFixedIncome": 60000, # monthlyFixedIncome derived from annualFixedIncome
    "annualVariableIncome": 6000, # monthlyVariableIncome derived from annualVariableIncome
    "annualRentalIncome": 0,
    "pledgedDeposit": 50000,
    "unpledgedDeposit": 0
}


debt_assessment_input = {
    "numberOfExistingPropertyLoans": 1,
    "monthlyCarLoan": 1556,
    "monthlyPropertyLoanInstalment": 0,
    "monthlyUnsecuredCredit": 0,
    "monthlySecuredRevolvingDebt": 0,
    "guarantorDebt": 685
}

debt_assessment_input_2 = {
    "numberOfExistingPropertyLoans": 0,
    "monthlyCarLoan": 0,
    "monthlyPropertyLoanInstalment": 0,
    "monthlyUnsecuredCredit": 0,
    "monthlySecuredRevolvingDebt": 0,
    "guarantorDebt": 0
}

borrower_1 = {
    "age": 30,
    "nationality": "Singaporean",
    "incomeUsedForCalculation": get_income_assessment_output(**income_assessment_input)['incomeUsedForCalculation'],
    "numberOfExistingPropertyLoans": 0,
    "existingPropertyCount": 0,
    # "existingPropertyType": "HDB",
    "debtUsedForCalculation": get_debt_assessment_output(**debt_assessment_input)['debtUsedForCalculation'],
}

borrower_2 = {
    "age": 28,
    "nationality": "Singaporean",
    "incomeUsedForCalculation": get_income_assessment_output(**income_assessment_input_2)['incomeUsedForCalculation'],
    "numberOfExistingPropertyLoans": 0,
    "existingPropertyCount": 0,
    # "existingPropertyType": None,
    "debtUsedForCalculation": get_debt_assessment_output(**debt_assessment_input_2)['debtUsedForCalculation'],
}

# property_type_input may be switched from "EC" to "private" if only one borrower
financial_position_summary_input = {
    "propertyType": property_type_input,
    "borrowers": [
        borrower_1,
        borrower_2,
    ]
}

loan_and_property_options_summary_input = {
    "propertyType": property_type_input,
    "loanTenure": get_financial_position_summary_output(**financial_position_summary_input)['maxLoanTenure'],
    "amountAvailableForPropertyLoanInstalment": get_financial_position_summary_output(**financial_position_summary_input)['amountAvailableForPropertyLoanInstalment'],
    "ltvRatio": get_financial_position_summary_output(**financial_position_summary_input)['maxLtvRatio'],
    "mediumTermInterestRate": 4,
    "borrowers": [
        borrower_1,
        borrower_2,
    ]
}


if __name__ == "__main__":
    print(get_income_assessment_output(**income_assessment_input))
    print(get_income_assessment_output(**income_assessment_input_2))
    print(get_debt_assessment_output(**debt_assessment_input))
    print(get_debt_assessment_output(**debt_assessment_input_2))
    print(get_financial_position_summary_output(**financial_position_summary_input))
    print(get_loan_and_property_options_summary_output(**loan_and_property_options_summary_input))
