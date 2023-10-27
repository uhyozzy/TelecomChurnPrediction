# import pandas as pd

# # 병합할 엑셀 파일의 파일 이름 및 경로
# file_paths = ["CustomerChurn.xlsx", "Telco_customer_churn.xlsx", "Telco_customer_churn_demographics.xlsx", "Telco_customer_churn_services.xlsx", "Telco_customer_churn_status.xlsx"]

# # 기준 엑셀 파일을 불러오기 (첫 번째 파일을 기준으로 사용)
# base_df = pd.read_excel(file_paths[0])

# # 나머지 엑셀 파일을 순서대로 불러와서 기준 엑셀 파일과 병합
# for file_path in file_paths[1:]:
#     df_to_merge = pd.read_excel(file_path)
    
#     # 중복된 열의 이름을 확인
#     common_columns = set(base_df.columns) & set(df_to_merge.columns)
    
#     # 중복된 열이 있는 경우, null 값을 다른 열의 값으로 채우기
#     for col in common_columns:
#         base_df[col].fillna(df_to_merge[col], inplace=True)
    
#     # 중복된 열을 제외한 나머지 열 추가
#     additional_columns = set(df_to_merge.columns) - common_columns
#     base_df = pd.concat([base_df, df_to_merge[list(additional_columns)]], axis=1)

# # 병합된 데이터프레임을 새로운 엑셀 파일로 저장
# base_df.to_excel("merged_file.xlsx", index=False)

import pandas as pd

# 병합할 엑셀 파일의 파일 이름 및 경로 리스트
file_paths = ["./data/Telco_customer_churn_demographics.xlsx", "./data/Telco_customer_churn_services.xlsx", "./data/Telco_customer_churn_status.xlsx"]

# 기준 엑셀 파일을 불러오기 (첫 번째 파일을 기준으로 사용)
base_df = pd.read_excel(file_paths[0])

# 나머지 엑셀 파일을 순서대로 불러와서 기준 엑셀 파일과 병합
for file_path in file_paths[1:]:
    df_to_merge = pd.read_excel(file_path)
    base_df = pd.merge(base_df, df_to_merge, on='Customer ID', how='inner')

# 병합된 데이터프레임을 새로운 엑셀 파일로 저장
base_df.to_excel("merged_file.xlsx", index=False)