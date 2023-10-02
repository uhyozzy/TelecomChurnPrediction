import pandas as pd
pip install plotly

import chart_studio
chart_studio.tools.set_credentials_file(username='username', api_key='api_key')
import chart_studio.plotly as py
import plotly.express as px

file_path = 'pre_file_re3.xlsx'
data = pd.read_excel(file_path)

data.info()
print('\n' + data.isnull().sum().to_string() + '\n')
print(data.groupby('Churn Value')['Customer ID'].nunique().to_string() + '\n')
print(data[data['Total Charges'].isna()])

fig = px.histogram(data, x="diff_in_charges",color = 'Contract',marginal="box")
fig.show()