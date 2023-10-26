import pandas as pd
import joblib

# 모델 학습 및 이탈확률 추가 함수. 데이터프레임 입력
def churn_prediction(df):

    # 데이터 원본 min, max값
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

    # 변환 함수
    def transform_and_scale(value, min_val, max_val):
        if value > max_val:
            return (value - max_val) / (max_val - min_val)
        elif value < min_val:
            return (value - min_val) / (max_val - min_val)
        else:
            return (value - min_val) / (max_val - min_val)

    # Membership 더미 변수 생성
    def create_membership_dummy(Membership):
        membership_dummy = {
            'Membership_None': 0,
            'Membership_Offer A': 0,
            'Membership_Offer B': 0,
            'Membership_Offer C': 0,
            'Membership_Offer D': 0,
            'Membership_Offer E': 0
        }
        membership_dummy['Membership_' + Membership] = 1
        return pd.Series(membership_dummy)

    # Contract 더미 변수 생성
    def create_contract_dummy(Contract):
        contract_dummy = {
            'Contract_Month-to-Month': 0,
            'Contract_One Year': 0,
            'Contract_Two Year': 0
        }
        contract_dummy['Contract_' + Contract] = 1
        return pd.Series(contract_dummy)

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
    
    train_df = df.copy()
    train_df = pd.concat([train_df, train_df['Membership'].apply(create_membership_dummy), train_df['Contract'].apply(create_contract_dummy)], axis=1)

    train_df['Scaled Data'] = train_df.apply(scale_data, axis=1)

    # 모델 로드
    loaded_model = joblib.load('./SGD_model.pkl')

    # 예측 및 결과 저장
    def predict_churn(row):
        scaled_data = row['Scaled Data']
        membership_dummy = row['Membership Dummy']
        contract_dummy = row['Contract Dummy']
        model_input = scaled_data + membership_dummy + contract_dummy
        churn_probability = loaded_model.predict_proba([model_input])[0][1] * 100  # 클래스 1의 확률을 선택
        return churn_probability

    train_df['Churn Probability'] = train_df.apply(predict_churn, axis=1)

    result_df = train_df[['Customer ID', 'Churn Probability']]

    # JSON 형식으로 변환
    json_df = result_df.to_json(orient='records')

    return json_df  # JSON 형식 반환

# 사용 파일 경로 지정
df = pd.read_excel("../Churn_final.xlsx")

# 결과를 저장할 데이터프레임 생성
result_df = df.copy()
result_df['Churn Probability'] = 0  # 빈 열 생성

for index, row in df.iterrows():
    # 각 행에 대한 예측을 수행
    churn_prob = churn_prediction(pd.DataFrame([row]))  # 현재 행만을 포함하는 데이터프레임을 생성하여 예측 함수 호출
    churn_prob = float(churn_prob[0]['Churn Probability'])  # JSON 결과에서 Churn Probability 값 추출
    result_df.at[index, 'Churn Probability'] = churn_prob  # 결과를 데이터프레임에 저장