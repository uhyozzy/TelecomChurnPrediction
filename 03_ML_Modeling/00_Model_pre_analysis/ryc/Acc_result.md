# Result
## Modeling score

### Method 1 : Split - Scaling - Encoding - Training

|No|Algoritm|Acc|Cross_val|Over_acc|Over_cross_val|
|--|--|--|--|--|--|
|1|Logistic|0.9461|0.9491|0.9333|0.9491|
|2|SVM-linear|0.9368|0.9404|0.9319|0.9404|
|3|SVM-rbf|0.9474|0.9507|0.9333|0.9507|
|4|Random Forest|0.9439|0.9553|0.9454|0.9553|
|5|Decision Tree|0.9326|0.9341|0.9184|0.9341|
|6|KNN|0.9269|0.9235|0.9127|0.9235|
|7|Naive Bayes|0.8290|0.8300|0.8254|0.8300|
|8|GBT|0.9475|0.9554|0.9468|0.9554|
|9|SGD|0.9404|0.9469|0.9432|0.9469|
|10|Adaboost|0.9461|0.9510|0.9425|0.9510|

---

### Method 2 : Scaling - Encoding - Split - Training

|No|Algoritm|Acc|Cross_val|Over_acc|Over_cross_val|
|--|--|--|--|--|--|
|1|Logistic|0.9375|0.9510|0.9262|0.9510|
|2|SVM-linear|0.9297|0.9428|0.9269|0.9428|
|3|SVM-rbf|0.9418|0.9503|0.9312|0.9503|
|4|Random Forest|0.9475|0.9537|0.9432|0.9537|
|5|Decision Tree|0.9290|0.9361|0.9319|0.9361|
|6|KNN|0.9155|0.9223|0.8985|0.9222|
|7|Naive Bayes|0.8481|0.8383|0.8389|0.8383|
|8|GBT|0.9475|0.9551|0.9347|0.9551|
|9|SGD|0.9120|0.9421|0.9155|0.9421|
|10|Adaboost|0.9461|0.9514|0.9375|0.9514|

---

10/10, 학습/검증 곡선 확인
10/11, xgboost, lightgbm 추가 확인
