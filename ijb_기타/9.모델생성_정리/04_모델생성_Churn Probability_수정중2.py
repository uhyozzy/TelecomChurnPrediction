import pandas as pd
import joblib
import warnings
# 경고를 무시
warnings.filterwarnings('ignore', category=UserWarning)

# 모델 학습 및 이탈확률 추가 함수. 데이터프레임 입력
def churn_prediction(df):
    
    # 데이터 원본 min, max값 - 데이터에서 직접 가져올수도 있을듯
    age_max = 80
    age_min = 19
    number_of_dependents_max = 9
    number_of_dependents_min = 0
    satisfaction_score_max = 5
    satisfaction_score_min = 1
    tech_services_max = 4
    tech_services_min = 0
    streaming_services_max = 2
    streaming_services_min = 0
    combined_product_max = 4
    combined_product_min = 1
    tenure_in_months_max = 72
    tenure_in_months_min = 1
    monthly_charge_max = 118.75
    monthly_charge_min = 18.25
    total_revenue_max = 11979.34
    total_revenue_min = 21.36

    # 스케일링 변환 함수
    def transform_and_scale(value, min_val, max_val):
        if value > max_val:
            return (value - max_val) / (max_val - min_val)
        elif value < min_val:
            return (value - min_val) / (max_val - min_val)
        else:
            return (value - min_val) / (max_val - min_val)
    
    # 더미 변수 생성
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
    
    # 더미 변수 생성
    def create_contract_dummy(Contract):
        contract_dummy = [0, 0, 0]  # Month-to-Month, One Year, Two Year에 대한 더미 변수

        if Contract == "Month-to-Month":
            contract_dummy[0] = 1
        elif Contract == "One Year":
            contract_dummy[1] = 1
        elif Contract == "Two Year":
            contract_dummy[2] = 1

        return contract_dummy
    
    # 데이터 스케일링
    def scale_data(row):
        scaled_data = []
        input_values = row[['Age', 'Number of Dependents', 'Satisfaction Score', 'Tech services',
                            'Streaming services', 'Combined Product', 'Tenure in Months',
                            'Monthly Charge', 'Total Revenue']]
        min_values = [age_min, number_of_dependents_min, satisfaction_score_min, tech_services_min,
                      streaming_services_min, combined_product_min, tenure_in_months_min,
                      monthly_charge_min, total_revenue_min]
        max_values = [age_max, number_of_dependents_max, satisfaction_score_max, tech_services_max,
                      streaming_services_max, combined_product_max, tenure_in_months_max,
                      monthly_charge_max, total_revenue_max]

        for i in range(len(input_values)):
            scaled_data.append(transform_and_scale(input_values[i], min_values[i], max_values[i]))

        return scaled_data

    # 예측 및 결과 저장
    def predict_churn(row):
        scaled_data = row['Scaled Data']
        membership_dummy = row['Membership Dummy']
        contract_dummy = row['Contract Dummy']
        model_input = scaled_data + membership_dummy + contract_dummy
        churn_probability = loaded_model.predict_proba([model_input])[0][1] * 100  # 클래스 1의 확률을 선택
        return churn_probability
    
    train_df = df.copy()
    train_df['Membership Dummy'] = train_df['Membership'].apply(create_membership_dummy)
    train_df['Contract Dummy'] = train_df['Contract'].apply(create_contract_dummy)

    train_df['Scaled Data'] = train_df.apply(scale_data, axis=1)

    # 모델 로드
    loaded_model = joblib.load('./SGD_model.pkl')

    train_df['Churn Probability'] = train_df.apply(predict_churn, axis=1)

    result_df = train_df[['Customer ID', 'Churn Probability']]

    # JSON 형식으로 변환
    json_df = result_df.to_json(orient='records')

    return json_df  # JSON 형식 반환

# 사용 파일 경로 지정
df = pd.read_excel("../Churn_final.xlsx")

# df 첫 행부터 마지막 행까지 예측 반복. (주의: 실행시 7천여개 전부 표시됨.)
# for i in range(len(df)):
#     churn_prob = churn_prediction(df.iloc[[i]])
#     print(churn_prob)

#100개만 출력
for i in range(0, 100):
    churn_prob = churn_prediction(df.iloc[[i]])
    print(churn_prob)

#이탈확률 수치가 원본파일과 비교했을때 일의 자리~소수점 자리 정도로 조금씩 다름.