#터미널에서 pip install scikit-learn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import SGDClassifier

#모델 학습 및 이탈확률 추가 함수. 데이터프레임 입력
def churn_prediction(df):
    
    train_df = df.copy()
    train_df = train_df.iloc[:,1:] # Customer ID 제외
    
    # 범주형 컬럼 One-Hot Encoding
    encoding_df = pd.get_dummies(train_df, columns=['Membership', 'Contract'])

    # 학습/테스트셋 분리
    y_target = encoding_df['Churn Value']
    X_data = encoding_df.drop(['Churn Value'], axis=1, inplace=False)

    X_train, X_test, y_train, y_test = train_test_split(X_data, y_target, test_size=0.2, random_state=156)

    # 학습 데이터셋(수치형 컬럼) 정규화
    ## Initialize variable
    X_train_origin, X_test_origin, y_train_origin, y_test_origin = X_train.copy(), X_test.copy(), y_train.copy(), y_test.copy()

    ## 수치형만 스케일링
    Numeric_column_list = []
    for i in range(len(X_data.columns)):
        if X_data[X_data.columns[i]].dtype == 'float64' or X_data[X_data.columns[i]].dtype == 'int64':
            Numeric_column_list.append(X_data.columns[i])
    numeric_train_data, numeric_test_data = X_train[Numeric_column_list], X_test[Numeric_column_list]
    scaler = MinMaxScaler()
    X_train[Numeric_column_list] = scaler.fit_transform(numeric_train_data)
    X_test[Numeric_column_list] = scaler.transform(numeric_test_data)

    # 선정한 모델로 학습
    best_model = SGDClassifier(random_state=42, alpha=0.001, loss='modified_huber',
                               max_iter=100, penalty='l1', tol=1e-05)
    best_model.fit(X_train, y_train)

    # 예측 결과 저장
    result_df = df.copy()
    result_df = result_df.iloc[:, 1:-1] # Customer ID, Churn Value 제외
    
    ## 범주형 컬럼 One-Hot Encoding
    encoding_test_data = pd.get_dummies(result_df, columns=['Membership', 'Contract'])
    
    ## 수치형만 정규화
    test_Numeric_column_list = []
    for i in range(len(encoding_test_data.columns)):
        if encoding_test_data[encoding_test_data.columns[i]].dtype == 'float64' or encoding_test_data[encoding_test_data.columns[i]].dtype == 'int64':
            test_Numeric_column_list.append(encoding_test_data.columns[i])         
    test_numeric_data = encoding_test_data[test_Numeric_column_list]
    scaler = MinMaxScaler()
    encoding_test_data[test_Numeric_column_list] = scaler.fit_transform(test_numeric_data)
    final_test_data = encoding_test_data
            
    # 최적의 모델을 사용하여 테스트 데이터의 클래스 확률을 예측합니다.
    predicted_probabilities = best_model.predict_proba(final_test_data)

    # 결과를 이탈확률(Churn Probability) 데이터프레임에 추가
    df['Churn Probability'] = predicted_probabilities[:, 1]*100  # 클래스 1의 확률을 선택

    # DataFrame에서 'Customer ID'와 '이탈확률(Churn Probability)' 열만 선택
    df_p = df[['Customer ID', 'Churn Probability']]

    # JSON 형식으로 변환
    json_df = df_p.to_json(orient='records')

    return json_df #JSON 형식 반환

#사용 파일 경로 지정
#df = pd.read_excel("../Churn_final.xlsx")

#함수 사용
#result = churn_prediction(df)

#print(result)
# 반환값 출력
# ...,"Churn Probability":26.4970288665},{"Customer ID":"3186-AJIEK","Churn Probability":0.0}]

# JSON 데이터를 문자열로 저장
#json_string = result
# 해당 문자열을 churn_predictions.json 파일로 저장
#with open("churn_predictions.json", "w") as json_file:
#    json_file.write(json_string)
