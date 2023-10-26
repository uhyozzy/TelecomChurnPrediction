# 데이터 개별 확률 계산
def single_row_predict(queryset, minmax_dict):
    satisfaction_score_max, satisfaction_score_min = 5, 1
    tech_services_max, tech_services_min = 4, 0
    streaming_services_max, streaming_services_min = 2, 0
    combined_product_max, combined_product_min = 4, 1

    # 최소/최대가 바뀔 수 있는 값들에 대해서 확인하여 변경하는 코드
    age_max, age_min = 80, 19
    if minmax_dict['age_max'] > age_max:
        age_max = minmax_dict['age_max']
    if minmax_dict['age_min'] < age_min:
        age_min = minmax_dict['age_min']

    number_of_dependents_max, number_of_dependents_min = 9, 0
    if minmax_dict['number_of_dependents_max'] > number_of_dependents_max:
        number_of_dependents_max = minmax_dict['number_of_dependents_max']
    if minmax_dict['number_of_dependents_min'] < number_of_dependents_min:
        number_of_dependents_min = minmax_dict['number_of_dependents_min']

    tenure_in_months_max, tenure_in_months_min = 72, 1
    if minmax_dict['tenure_in_months_max'] > tenure_in_months_max:
        tenure_in_months_max = minmax_dict['tenure_in_months_max']
    if minmax_dict['tenure_in_months_min'] < tenure_in_months_min:
        tenure_in_months_min = minmax_dict['tenure_in_months_min']

    monthly_charge_max, monthly_charge_min = 118.75, 18.25
    if minmax_dict['monthly_charge_max'] > monthly_charge_max:
        monthly_charge_max = minmax_dict['monthly_charge_max']
    if minmax_dict['monthly_charge_min'] < monthly_charge_min:
        monthly_charge_min = minmax_dict['monthly_charge_min']

    total_revenue_max, total_revenue_min = 11979.34, 21.36
    if minmax_dict['total_revenue_max'] > total_revenue_max:
        total_revenue_max = minmax_dict['total_revenue_max']
    if minmax_dict['total_revenue_min'] < total_revenue_min:
        total_revenue_min = minmax_dict['total_revenue_min']
    # 최소/최대가 바뀔 수 있는 값들에 대해서 확인하여 변경하는 코드 종료

    # Min-Max Scaling 직접 구현
    # 공식은 다음과 같다. : (x - x_min) / (x_max - x_min)
    def transform_and_scale(value, min_val, max_val):
        if value > max_val:  # 기존 최대치보다 입력 값이 높을 때
            return (value - min_val) / (value - min_val)
        elif value < min_val:  # 기존 최소치보다 입력 값이 낮을 때
            return (value - value) / (max_val - value)
        else:
            return (value - min_val) / (max_val - min_val)

    def create_membership_dummy(Membership):
        membership_dummy = [0, 0, 0, 0, 0, 0]  # None, Offer A, Offer B, Offer C, Offer D, Offer E에 대한 더미 변수

        if Membership == "None":
            membership_dummy[0] = 1
        elif Membership == "Offer A":
            membership_dummy[1] = 1
        elif Membership == "Offer B":
            membership_dummy[2] = 1
        elif Membership == "Offer C":
            membership_dummy[3] = 1
        elif Membership == "Offer D":
            membership_dummy[4] = 1
        elif Membership == "Offer E":
            membership_dummy[5] = 1

        return membership_dummy

    def create_contract_dummy(Contract):
        contract_dummy = [0, 0, 0]  # Month-to-Month, One Year, Two Year에 대한 더미 변수

        if Contract == "Month-to-Month":
            contract_dummy[0] = 1
        elif Contract == "One Year":
            contract_dummy[1] = 1
        elif Contract == "Two Year":
            contract_dummy[2] = 1

        return contract_dummy

    predict_target_data = []

    # 개별 결과값을 리스트에 입력
    predict_target_data.append(transform_and_scale(queryset.age, age_min, age_max))
    predict_target_data.append(transform_and_scale(queryset.tbservice.number_of_dependents, number_of_dependents_min, number_of_dependents_max))
    predict_target_data.append(transform_and_scale(queryset.satisfaction_score, satisfaction_score_min, satisfaction_score_max))
    predict_target_data.append(transform_and_scale(queryset.tbservice.tech_services, tech_services_min, tech_services_max))
    predict_target_data.append(transform_and_scale(queryset.tbservice.streaming_services, streaming_services_min, streaming_services_max))
    predict_target_data.append(transform_and_scale(queryset.tbservice.combined_product, combined_product_min, combined_product_max))
    predict_target_data.append(transform_and_scale(queryset.tbcontract.tenure_in_months, tenure_in_months_min, tenure_in_months_max))
    predict_target_data.append(transform_and_scale(queryset.tbcontract.monthly_charge, monthly_charge_min, monthly_charge_max))
    predict_target_data.append(transform_and_scale(queryset.tbcontract.total_revenue, total_revenue_min, total_revenue_max))
    
    # membership, contract는 애초에 list라서, append를 하면 리스트 그대로 입력됨. 따라서 리스트 합으로 연결
    predict_target_data = predict_target_data+(create_membership_dummy(queryset.membership))
    predict_target_data = predict_target_data+(create_contract_dummy(queryset.tbcontract.contract))

    return predict_target_data  # 리스트 형식으로 출력됨, proba가 받는 형식이 list