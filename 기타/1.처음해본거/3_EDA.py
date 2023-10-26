import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# 엑셀 파일 불러오기
file_path = 'pre_file_re3.xlsx'
data = pd.read_excel(file_path)

columns = data.columns.tolist()


dellist = ['Customer ID']
for i in dellist:
    columns.remove(i)

# subplot 설정
num_rows = math.ceil(len(columns) / 4)
fig, axes = plt.subplots(num_rows, 4, figsize=(25, 6 * num_rows))
    

for i, col in enumerate(columns):
    row = i // 4
    col_num = i % 4
    
    unique_categories = len(data[col].unique())

    # 각 열에 대한 수평 막대 그래프 또는 파이 차트 생성
    if len(data[col].unique()) > 10:  # 카테고리가 많으면 수평 막대 그래프로 표시
        sns.countplot(x=col, data=data, ax=axes[row, col_num], palette="Blues_d")
    else:  # 카테고리가 적으면 파이 차트로 표시
        data_count = data[col].value_counts()
        labels = data_count.index
        values = data_count.values
        axes[row, col_num].pie(values, labels=labels, autopct='%0.2f%%', startangle=140)
    
    axes[row, col_num].set_title(col)

# 레이아웃 조정
plt.tight_layout()
#plt.show()

# 저장
plt.savefig('EDA_plot.pdf')
plt.close()
