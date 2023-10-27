import pandas as pd

# 엑셀 파일 불러오기
file_path = 'pre_file_re_re.xlsx'
data = pd.read_excel(file_path)

# 카테고리형 IBM 설명 페이지 순서대로 0, 1, 2, 3, 4, 5 순으로 변환
data = data.replace({'Offer A' : 1, 'Offer B' : 2, 'Offer C' : 3, 'Offer D' : 4, 'Offer E' : 5, 'DSL' : 1, 'Fiber Optic' : 2, 'Cable' : 3, 'Month-to-Month' : 0, 'One Year' : 1, 'Two Year' : 2, 'Bank Withdrawal' : 0, 'Credit Card' : 1, 'Mailed Check' : 2, 'Churned' : 0, 'Stayed' : 2, 'Joined' : 3, 'Attitude' : 1, 'Competitor' : 2, 'Dissatisfaction' : 3, 'Price' : 4, 'Other' : 5})

# 수정된 데이터를 새로운 엑셀 파일로 저장
output_file_path = 'pre_file_re3.xlsx'
data.to_excel(output_file_path, index=False)