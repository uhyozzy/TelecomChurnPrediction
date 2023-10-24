from django.shortcuts import render, redirect
from .models import TbUser, TbService, TbContract
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .module.create_functions import pagination, customer_create, dashboard_management, marketing_suggest
from .module.administration import single_row_predict
from django.db.models import Min, Max, Avg
from .apps import TelcoDefenceConfig  # Mechine Learning pre-load
# import numpy as np
# from PIL import Image

# Create your views here.
def test(request):  # 읽기 테스트, paginator 추가(23.10.17~18)
    # tp = TbUser.objects.all()
    # tp = TbUser.objects.filter(satisfaction_score=1).order_by('customer_id')
    # tp = TbUser.objects.filter(customer_id='0004-TLHLJ').select_related('tbcontract').order_by('customer_id')
    tp = TbUser.objects.filter(customer_id='0004-TLHLJ')
    # tp = TbUser.objects.filter(customer_id='1')

    testing = TbUser.objects.aggregate(age_max=Max('age'), age_min=Min('age'))

    # number_of_dependents_max, number_of_dependents_min = 9, 0
    # tenure_in_months_max, tenure_in_months_min = 72, 1
    # monthly_charge_max, monthly_charge_min = 118.75, 18.25
    # total_revenue_max, total_revenue_min = 11979.34, 21.36

    print(testing)
    print(tp[0].tbcontract.contract)

    # print(tp.query)  # SQL 확인용
    page = request.GET.get('page')
    lines, paginator, custom_range = pagination(tp, page)

    context = {"testing_point": tp, 
               "lines": lines,  # paginator 결과
               "paginator": paginator,  # paginator 데이터
               "custom_range": custom_range,  # 페이지 길어지는 것 방지
               "end_page": paginator.num_pages,  # 마지막 페이지 확인
               "paginator_idx": paginator.num_pages - 2,  # 마지막 페이지 가까울 때 중복 출력 방지용 기준점
               }

    return render(request, 'testing_page/index.html', context)


def inputtest(request):  # 입력 테스트(23.10.17~18)
    if request.method == 'GET':
        test_context = "This is test sentence."
        return render(request, 'testing_page/inputtest.html', {"test_context": test_context})
    else:
        word = request.POST.get('testing')
        return redirect('itt_a')

        # predict_model pre-load react
        # word = request.POST.get('predict_order')
        # # print(eval(word), type(eval(word)))
        # test_data = eval(word)
        # test_data = np.array(test_data).reshape(1, -1)
        # predict_result = TelcoDefenceConfig.mlmodels.predict_proba(test_data)
        # return render(request, 'testing_page/inputtest.html', {"predict_result": predict_result})
        # test_data : [0.68852, 0.00000, 0.5, 0.0000, 0.0000, 1.0, 0.23944,  0.01791, 0.06277, 1, 0,0,0,0,0,1,0,0]


def savetest(request):  # 신규 생성 및 DB 반영 테스트 진행(23.10.18)
    if request.method == 'GET':
        return render(request, 'testing_page/savetest.html')
    else:
        argu_list = {"customer_id": 0, "age": 0, "satisfaction_score": 0, "membership": 0, "churn_value": 0,
                     "contract": 0, "tenure_in_months": 0, "monthly_charge": 0, "total_revenue": 0, "tech_services": 0,
                     "streaming_services": 0, "combined_product": 0, "number_of_dependents": 0}
        for i in argu_list.keys():
            argu_list[i] = request.POST.get(i)

        customer_create(request)  # 생성 함수
        return redirect('stt')

# 필요한 기능 정리(23.10.18)
'''
- 필수
1. 1. 메인 페이지 렌더링
    - 단순 렌더링이므로 중요도 낮음
2. 세부 페이지 탬플릿 분리 및 블럭화
    - 사이드바 등 고정적으로 나오는 구문에 대해서 분리/블럭화하여 재사용성 향상
3. 전체 유저에 대한 리스트
    - 리스트 출력 및 쿼리 내용 테스트 완료 > 실제 탬플릿과 연동시키기 필요
    - 탬플릿 블록화(함수화) 진행 중
4. 유저 세부 정보
    - 아이디 링크를 통하여 접속한 페이지, 별도 접근 방식 미구현 예정
    - 해지확률 및 마케팅 정보 제공 페이지
5. 신규 유저 정보 입력
    - 입력 테스트 완료 > 저장하여 DB에 반영되는지 테스트 진행중
    - 
6. 기존 유저 정보 수정
7. 대시보드 계산 및 렌더링

- 추가?
    - 변동 로그 확인하여 증감확인 > 중요한 유저 증가시 유저 리스트에 얼럿
    -

- 변경 필요사항
    - 모델에 Validation 추가해야 함(231018)
    - 모델에 default 값도 추가해야 함(231019)
    - CLTV 통계 모델 추가, user 모델에 CLTV 추가(231019)

    - 코드 정리
'''


def main_page_render(request):  # 시작시 보여지는 메인페이지 렌더링
    return render(request, 'home.html')


def customer_list(request):  # 전체 고객 리스트 출력
    if request.method == 'GET':
        filtering_order = request.GET.get('filtering_order')

        if filtering_order == "all":  # filtering, random output
            list_data = TbUser.objects.all().order_by("?")
        elif filtering_order == "upper40":
            list_data = TbUser.objects.filter(churn_proba__gte=40).order_by("?")
        elif filtering_order == "upper60":
            list_data = TbUser.objects.filter(churn_proba__gte=60).order_by("?")
        elif filtering_order == "potential":
            list_data = TbUser.objects.filter(churn_proba_group="Potential").order_by("?")
        elif filtering_order == "high":
            list_data = TbUser.objects.filter(churn_proba_group="High").order_by("?")
        else:
            filtering_order = "all"
            list_data = TbUser.objects.all().order_by("?")

        filtered_name_dict = {"all": "없음", 
                              "upper40": "이탈 확률 40% 이상", 
                              "upper60": "이탈 확률 60% 이상", 
                              "potential": "잠재 이탈자 그룹", 
                              "high": "고위험 그룹",
                              }

        proba_avg = TbUser.objects.aggregate(Avg('churn_proba'))['churn_proba__avg']
        page = request.GET.get('page')
        lines, paginator, custom_range = pagination(list_data, page)

        context = {"list_data": list_data, 
                   "lines": lines,  # paginator 결과
                   "paginator": paginator,  # paginator 데이터
                   "custom_range": custom_range,  # 페이지 길어지는 것 방지
                   "end_page": paginator.num_pages,  # 마지막 페이지 확인
                   "paginator_idx": paginator.num_pages - 2,  # 마지막 페이지 가까울 때 중복 출력 방지용 기준점
                   "filtering_order_name": filtered_name_dict[filtering_order],
                   "proba_avg": proba_avg,
                   }

        return render(request, 'list.html', context)


def customer_detail(request):  # 고객 ID를 통한 세부 고객 정보 페이지 단순 출력

    context = {"text": "먼저 고객을 검색하세요", 
               "c_id": None,
               }

    return render(request, "detail.html", context)


def customer_detail_selected(request, customer_ids=0):  # 리스트 페이지 고객 ID를 링크를 통한 세부 고객 정보 출력
    data = TbUser.objects.filter(customer_id=customer_ids)

    cltv_value = list(TbUser.objects.filter(customer_id=customer_ids).values())[0]['cltv']
    tr_value = list(TbContract.objects.filter(customer_id=customer_ids).values())[0]['total_revenue']
    tm_value = list(TbContract.objects.filter(customer_id=customer_ids).values())[0]['tenure_in_months']
    nod_value = list(TbService.objects.filter(customer_id=customer_ids).values())[0]['number_of_dependents']

    suggestion_text = marketing_suggest(cltv_value, tr_value, tm_value, nod_value)

    context = {"text": suggestion_text, 
               "c_id": customer_ids, 
               "data": data}

    return render(request, "detail.html", context)


def customer_detail_search(request, customer_ids=0):  # 고객 정보 페이지의 검색창을 통한 세부 고객 정보 출력
    checkpoint = request.GET.get("input_cs_id")
    if checkpoint == "":
        return redirect('customer-detail')

    else:
        data = TbUser.objects.filter(customer_id=checkpoint)

        if data.exists():
            cltv_value = list(TbUser.objects.filter(customer_id=checkpoint).values())[0]['cltv']
            tr_value = list(TbContract.objects.filter(customer_id=checkpoint).values())[0]['total_revenue']
            tm_value = list(TbContract.objects.filter(customer_id=checkpoint).values())[0]['tenure_in_months']
            nod_value = list(TbService.objects.filter(customer_id=checkpoint).values())[0]['number_of_dependents']

            suggestion_text = marketing_suggest(cltv_value, tr_value, tm_value, nod_value)

            context = {"text": suggestion_text, 
                       "c_id": checkpoint, 
                       "data": data}
            return render(request, 'detail.html', context)
        else:
            return redirect('customer-detail')


def dashboard(request):  # 시각화
    viewing_dict = {
                    "user": "/static/images/category_user.png", 
                    "service": "/static/images/category_service.png", 
                    "contract": "/static/images/category_contract.png"
                    }

    viewing_key = request.GET.get('dropdown_select')

    if viewing_key is None:
        viewing_key = 'user'
        viewing = viewing_dict["user"]
    else:
        viewing = viewing_dict[viewing_key]

    context = {"now_view": viewing, }

    if viewing_key == 'user':
        data = TbUser.objects.values_list('age', 'membership', 'satisfaction_score', 'cltv', 'churn_value')
        dashboard_management(viewing_key, data)
        output_context = {"title1": "나이 비율", "desc1": "연령별 가입자 분포 그래프",
                          "title2": "멤버십 가입 비율", "desc2": "멤버십별 가입자 분포 그래프",
                          "title3": "고객 관리 점수 비율", "desc3": "고객 관리 점수별 가입자 분포 그래프",
                          "title4": "고객 점수 비율", "desc4": "고객 점수별 가입자 분포 그래프",
                          "title5": "나이-해지 상관관계", "desc5": "연령과 해지여부 사이의 상관관계 그래프",
                          "title6": "멤버십-해지 상관관계", "desc6": "멤버십 종류와 해지여부 사이의 상관관계 그래프",
                          "title7": "고객 관리 점수-해지 상관관계", "desc7": "고객 관리 점수와 해지여부 사이의 상관관계 그래프",
                          "title8": "고객 점수-해지 상관관계", "desc8": "고객 점수와 해지여부 사이의 상관관계 그래프",
                          }

    elif viewing_key == 'service':
        data = TbUser.objects.select_related('tbservice').values_list('tbservice__tech_services', 'tbservice__streaming_services', 
                                                                      'tbservice__number_of_dependents', 'tbservice__combined_product', 'churn_value')

        dashboard_management(viewing_key, data)
        output_context = {"title1": "기술 서비스 비율", "desc1": "기술 서비스 가입자 분포 그래프",
                          "title2": "부가 서비스 비율", "desc2": "부가 서비스 가입자 분포 그래프",
                          "title3": "가족 결합 수 비율", "desc3": "가족 결합 수 별 가입자 분포 그래프",
                          "title4": "결합 상품 수 비율", "desc4": "결합 상품 수 별 가입자 분포 그래프",
                          "title5": "기술 서비스-해지 상관관계", "desc5": "기술 서비스 가입 상태와 해지여부 사이의 상관관계 그래프",
                          "title6": "부가 서비스-해지 상관관계", "desc6": "부가 서비스 가입 상태와 해지여부 사이의 상관관계 그래프",
                          "title7": "가족 결합 수-해지 상관관계", "desc7": "가족 결합 수와 해지여부 사이의 상관관계 그래프",
                          "title8": "결합 상품 수-해지 상관관계", "desc8": "결합 상품 수와 해지여부 사이의 상관관계 그래프",
                          }

    elif viewing_key == 'contract':
        data = TbUser.objects.select_related('tbcontract').values_list('tbcontract__contract', 'tbcontract__tenure_in_months', 
                                                                       'tbcontract__monthly_charge', 'tbcontract__total_revenue', 'churn_value')

        dashboard_management(viewing_key, data)
        output_context = {"title1": "계약 형태", "desc1": "계약 상태별 가입자 분포 그래프",
                          "title2": "가입 개월 수", "desc2": "가입 개월수 별 가입자 분포 그래프",
                          "title3": "기본 요금", "desc3": "기본 요금 분포별 가입자 분포 그래프",
                          "title4": "총 요금", "desc4": "총 요금 분포별 가입자 분포 그래프",
                          "title5": "계약 형태-해지 상관관계", "desc5": "계약 상태와 해지여부 사이의 상관관계 그래프",
                          "title6": "가입 개월 수-해지 상관관계", "desc6": "가입 개월 수와 해지여부 사이의 상관관계 그래프",
                          "title7": "기본 요금-해지 상관관계", "desc7": "기본 요금와 해지여부 사이의 상관관계 그래프",
                          "title8": "총 요금-해지 상관관계", "desc8": "총 요금와 해지여부 사이의 상관관계 그래프",
                          }

    context.update(output_context)

    return render(request, 'dashboard.html', context)


# 확률 재계산용 함수
def re_calc(request):
    import numpy as np
    import pandas as pd

    if request.method == "GET":
        return render(request, 'administrator.html')

    elif request.method == "POST":
        execute_order = request.POST.get('order')
        if execute_order == 'recalc':
            column_name = ["Age", "Number of Dependents", "Satisfaction Score", "Tech services", "Streaming services",
                           "Combined Product", "Tenure in Months", "Monthly Charge", "Total Revenue", "Membership_None",
                           "Membership_Offer A", "Membership_Offer B", "Membership_Offer C", "Membership_Offer D", "Membership_Offer E",
                           "Contract_Month-to-Month", "Contract_One Year", "Contract_Two Year",]

            queryset = TbUser.objects.all()

            mmdict = TbUser.objects.aggregate(age_max=Max('age'), age_min=Min('age'), 
                        satisfaction_score_max=Max('satisfaction_score'), satisfaction_score_min=Min('satisfaction_score'))
            mmdict.update(TbService.objects.aggregate(number_of_dependents_max=Max('number_of_dependents'), number_of_dependents_min=Min('number_of_dependents'), 
                            tech_services_max=Max('tech_services'), tech_services_min=Min('tech_services'),
                            streaming_services_max=Max('streaming_services'), streaming_services_min=Min('streaming_services'), 
                            combined_product_max=Max('combined_product'), combined_product_min=Min('combined_product')))
            mmdict.update(TbContract.objects.aggregate(tenure_in_months_max=Max('tenure_in_months'), tenure_in_months_min=Min('tenure_in_months'), 
                            monthly_charge_max=Max('monthly_charge'), monthly_charge_min=Min('monthly_charge'), 
                            total_revenue_max=Max('total_revenue'), total_revenue_min=Min('total_revenue')))

            for i in range(len(queryset)):
                proba_list = single_row_predict(queryset[i], mmdict)

                predict_data = pd.DataFrame(data=np.array(proba_list).reshape(1, -1), columns=column_name)
                predict_result = TelcoDefenceConfig.mlmodels.predict_proba(predict_data)[0][1] * 100

                target_row = TbUser.objects.get(customer_id=queryset[i].customer_id)

                target_row.churn_proba = round(predict_result, 4)

                if predict_result >= 60:
                    target_row.churn_proba_group = 'High'
                elif predict_result >= 40:
                    target_row.churn_proba_group = 'Potential'
                else:
                    target_row.churn_proba_group = 'Stable'

                target_row.save()
        return redirect('administration_page')


""" 나중 테스트 희망 
detail page
    if request.method == "GET":
        cs_id = request.GET.get('input_cs_id')
        print("cs_id:",cs_id, type(cs_id))
        if cs_id == "None":
            c_id = "not exist"
        elif cs_id == "":
            c_id = "not exist"
        else:
            c_id = customer_ids

        print("c_id :",c_id, type(c_id), type(c_id) is None)
        if c_id == "not exist":
            return redirect('customer-detail')
            # return render(request, 'detail.html')
        elif c_id == cs_id:
            data = TbUser.objects.filter(customer_id=c_id)
            print(data.exists())
            if data.exists():
                context = {"text": "This is marketing recommand", 
                           "c_id": c_id, 
                           "data": data}
                return render(request, 'detail.html', context)
            else:
                print("here1")
                return redirect('customer-detail')
        else:
            print("here2")
            render(request, 'detail.html')

    # elif request.method == "POST":  # 231020, only get method One-def failed...
    #     c_id = request.POST.get('input_cs_id')

    #     if c_id == "":
    #         return redirect('customer-detail')
    #     else:
    #         print(c_id, type(c_id))
    #         data = TbUser.objects.filter(customer_id=c_id)

    #         context = {"text": "This is marketing recommand", 
    #                    "c_id": c_id, 
    #                    "data": data}

    #         print(context["c_id"])
    #         return render(request, 'detail.html', context)
"""
