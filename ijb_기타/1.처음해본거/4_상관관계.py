import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 엑셀 파일 불러오기
file_path = 'pre_file_re3.xlsx'
data = pd.read_excel(file_path)

# Customer ID 열 삭제
data.drop('Customer ID', axis=1, inplace=True)

# 컬럼 간 상관관계 계산
correlation_matrix = data.corr()

# 상관관계 히트맵 시각화
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
plt.title('CC heatmap')
#plt.show()

#저장
plt.savefig('CC_heatmap.png')
plt.close()