import pandas as pd

# # 데이터를 불러오기
# data = pd.read_excel("merged_file.xlsx")

# # 'Service ID'와 'Customer ID' 열을 제외한 열을 수치화하기
# columns_to_convert = ['Referred a Friend', 'Phone Service', 'Multiple Lines', 'Online Security', 
#                       'Online Backup', 'Device Protection Plan', 'Premium Tech Support', 
#                       'Streaming TV', 'Streaming Movies', 'Streaming Music', 'Unlimited Data', 
#                       'Paperless Billing']

# # 'Yes'를 1로, 'No'를 0으로 매핑
# for col in columns_to_convert:
#     data[col] = data[col].map({'Yes': 1, 'No': 0})

# # 'Gender' 열을 수치화 (Female을 1로, Male을 0으로)
# data['Gender'] = data['Gender'].map({'Female': 1, 'Male': 0})

# # 'Internet Type' 열을 카테고리 값으로 수치화
# data['Internet Type'] = data['Internet Type'].astype('category').cat.codes

# # 'Count'와 'Quarter' 열을 카테고리 값으로 수치화
# data['Count'] = data['Count'].astype('category').cat.codes
# data['Quarter'] = data['Quarter'].astype('category').cat.codes

# # 수정된 데이터를 저장하기
# data.to_excel("preprocessed_data.xlsx", index=False)

# 엑셀 파일 불러오기
file_path = 'merged_file.xlsx'
data = pd.read_excel(file_path)

# 모든 열에 대해 null 값을 0으로 채우기
data = data.fillna(0)

# 'Yes'를 1로, 'No'를 0으로 변환
data = data.replace({'Yes': 1, 'No': 0})

# '여'를 1로, '남'을 0으로 변환
data['Gender'] = data['Gender'].replace({'Female': 1, 'Male': 0})

# 문자열로 표현된 숫자를 정수로 변환
columns_to_convert = ['Count', 'Age', 'Number of Dependents', 'Number of Referrals', 'Tenure in Months', 'Avg Monthly GB Download', 'Satisfaction Score', 'Churn Value', 'Churn Score', 'CLTV']
data[columns_to_convert] = data[columns_to_convert].astype(int)

# 수정된 데이터를 새로운 엑셀 파일로 저장
output_file_path = 'pre_file.xlsx'
data.to_excel(output_file_path, index=False)