# 김소희님 작업물
# 라이브러리 로드

'''plotly 설치
pip install plotly
pip install kaleido==0.1.0post1
'''

import plotly.express as px
import pandas as pd
import numpy as np


# 데이터 로드

df = pd.read_excel("Churn_final.xlsx")

# CLTV 컬럼 추가
cltv_df = pd.read_excel("total.xlsx")
df['CLTV'] = cltv_df['CLTV']

print(df.head())

# 1. 유저 기본 정보

# 1-1. 기본 통계 그래프

def user_chart_stat(df):
    user_x_cols = ['Age', 'Membership', 'Satisfaction Score', 'CLTV']

    fig = None  # 먼저 fig를 None으로 초기화

    for user_x_col in user_x_cols:
        if user_x_col == "Age":
            fig = px.histogram(df, x=user_x_col, nbins=100)
            # 그래프 레이아웃 설정
            fig.update_layout(
                xaxis_title=user_x_col,  # x_col 변수를 그래프의 x축 레이블로 설정
                yaxis_title='고객 수(명)',
                bargap=0.2)
            #fig.show()
            fig.write_image("user_stat_Age.png")

        elif user_x_col == 'Membership':
            fig = px.pie(df, names='Membership',
                         color_discrete_sequence=["#2E52C0", "#3664BC", "#3873C1", "#5398D9", "#91C3F4", "aliceblue"])
            fig.update_traces(textinfo='label+percent', textfont_size=15, hole=.3)
            fig.update_layout(title_text='Membership 가입 비율', title_y=0.95, title_x=0.5, showlegend=False)
            #fig.show()
            fig.write_image("user_stat_Membership.png")

        else:
            fig = px.histogram(df, x=user_x_col, nbins=5)
            # 그래프 레이아웃 설정
            fig.update_layout(
                xaxis_title=user_x_col,  # x_col 변수를 그래프의 x축 레이블로 설정
                yaxis_title='고객 수(명)',
                bargap=0.2)
            #fig.show()
            fig.write_image(f"user_stat_{user_x_col}.png")

# 유저 기본 정보_기본 통계 그래프 함수 호출
user_chart_stat(df)


# 1-2. 상관관계 그래프

def user_chart_corr(df):
    user_x_cols = ['Age', 'Membership', 'Satisfaction Score', 'CLTV']
    for user_x_col in user_x_cols:
        if user_x_col == 'CLTV':
            fig = px.histogram(df, x=user_x_col, y="Churn Value", histfunc='avg', nbins=5)
            fig.update_layout(xaxis_title='CLTV', yaxis_title='Churn Value', bargap=0.2)

            colors = ["#4A55A2", "#7895CB", "#A0BFE0", "#C5DFF8", "aliceblue"]
            fig.update_traces(marker_color=colors)
            #fig.show()
            fig.write_image(f"user_corr_{user_x_col}.png")

        else:
            fig = px.bar(df.groupby(user_x_col)['Churn Value'].mean().reset_index(),
                         x=user_x_col, y='Churn Value', color="Churn Value",
                         color_continuous_scale=px.colors.sequential.Blues)
            #fig.show()
            fig.write_image(f"user_corr_{user_x_col}.png")

# 유저 기본 정보_상관관계 그래프 함수 호출
user_chart_corr(df)

# 2. 서비스 정보

# 2-1. 기본 통계 그래프
def service_chart_stat(df):
    service_x_cols = ['Tech services', 'Streaming services', 'Number of Dependents', 'Combined Product']

    for service_x_col in service_x_cols:

        fig = px.pie(df, names=service_x_col,
                     color_discrete_sequence=["#2E52C0", "#3664BC", "#3873C1", "#5398D9", "#91C3F4", "aliceblue"])
        fig.update_traces(textinfo='label+percent', textfont_size=15, hole=.3)

        if service_x_col == 'Number of Dependents':
            fig.update_layout(title_text="가족 결합 수", title_y=0.95, title_x=0.5)
            fig.update_layout(showlegend=False)
            #fig.show()
            fig.write_image(f"user_stat_{service_x_col}.png")
        else:
            fig.update_layout(title_text=f"{service_x_col} 이용 수", title_y=0.95, title_x=0.5)
            fig.update_layout(showlegend=False)
            #fig.show()
            fig.write_image(f"service_stat_{service_x_col}.png")

# 서비스 정보_기본 통계 그래프 함수 호출
service_chart_stat(df)

# 2-2. 상관관계 그래프

def service_chart_corr(df):
    service_x_cols = ['Tech services', 'Streaming services','Number of Dependents', 'Combined Product']

    for service_x_col in service_x_cols:
        fig = px.bar(df.groupby(service_x_col)['Churn Value'].mean().reset_index(), x=service_x_col, y='Churn Value',
                     color="Churn Value", color_continuous_scale=px.colors.sequential.Blues)

        # x축의 단위를 1로 설정
        fig.update_xaxes(dtick=1)

        #fig.show()
        fig.write_image(f"service_corr_{service_x_col}.png")

# 서비스 정보_상관관계 그래프 함수 호출
service_chart_corr(df)


# 3. 요금제 정보

# 3-1. 기본 통계 그래프

def bill_chart_stat(df):
    bill_x_cols = ['Contract', 'Tenure in Months', 'Monthly Charge', 'Total Revenue']

    for bill_x_col in bill_x_cols:
        if bill_x_col == 'Contract':
            fig = px.pie(df, names=bill_x_col,
                        color_discrete_sequence=["#2E52C0", "#3664BC", "#3873C1", "#5398D9", "#91C3F4", "aliceblue"])
            fig.update_traces(textinfo='label+percent', textfont_size=15, hole=.3)
            fig.update_layout(title_text="계약 형태", title_y=0.95, title_x=0.5, showlegend=False)
            #fig.show()
            fig.write_image(f"bill_stat_{bill_x_col}.png")
        else:
            fig = px.histogram(df, x=bill_x_col, nbins=10)
             # 그래프 레이아웃 설정
            fig.update_layout(
            xaxis_title=bill_x_col,  # x_col 변수를 그래프의 x축 레이블로 설정
            yaxis_title='고객 수(명)',
            bargap=0.2)
            #fig.show()
            fig.write_image(f"bill_stat_{bill_x_col}.png")

# 요금제 정보_기본 통계 그래프 함수 호출
bill_chart_stat(df)


# 3-2. 상관관계 그래프

def bill_chart_corr(df):
    bill_x_cols = ['Contract', 'Tenure in Months', 'Monthly Charge', 'Total Revenue']

    for bill_x_col in bill_x_cols:

        if bill_x_col == 'Contract' or bill_x_col == 'Tenure in Months':
            fig = px.bar(df.groupby(bill_x_col)['Churn Value'].mean().reset_index(), x=bill_x_col, y='Churn Value'
                         , color="Churn Value",
                         color_continuous_scale=px.colors.sequential.Blues)
            #fig.show()
            fig.write_image(f"bill_corr_{bill_x_col}.png")
        elif bill_x_col == 'Monthly Charge':
            fig = px.histogram(df, x=bill_x_col, y="Churn Value", histfunc='avg', nbins=10)
            fig.update_layout(xaxis_title=bill_x_col, yaxis_title='Churn Value', bargap=0.2)
            colors = ["aliceblue", "#91C3F4", "#5398D9", "#3664BC", "#2E52C0", "#3873C1"]
            fig.update_traces(marker_color=colors)
            #fig.show()
            fig.write_image(f"bill_corr_{bill_x_col}.png")
        else:
            fig = px.histogram(df, x=bill_x_col, y="Churn Value", histfunc='avg', nbins=50)
            fig.update_layout(xaxis_title=bill_x_col, yaxis_title='Churn Value', bargap=0.2)
            #fig.show()
            fig.write_image(f"bill_corr_{bill_x_col}.png")

# 요금제 정보_상관관계 그래프 함수 호출
bill_chart_corr(df)