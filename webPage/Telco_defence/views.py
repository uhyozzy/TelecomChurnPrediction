### Lib import ###
# django lib
from django.shortcuts import render, redirect
from django.db.models import Min, Max, Avg

# apps files
from .models import TbUser, TbService, TbContract
from .module.create_functions import pagination, dashboard_management, marketing_suggest
from .module.administration import single_row_predict
from .apps import TelcoDefenceConfig  # Machine Learning pre-load

''' 필요한 기능 정리(23.10.18)
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
5. 신규 유저 정보 입력(취소)
    - 입력 테스트 완료 > 저장하여 DB에 반영되는지 테스트 진행중
6. 기존 유저 정보 수정(취소)
7. 대시보드 계산 및 렌더링

- 추가?
    - 변동 로그 확인하여 증감확인 > 중요한 유저 증가시 유저 리스트에 얼럿(취소)
'''


def main_page_render(request):  # 시작시 보여지는 메인페이지 렌더링
    request.session['filtering_order'] = None  # List 페이지 관련 세션 정리

    return render(request, 'home.html')


def customer_list(request):  # 전체 고객 리스트 출력
    if request.method == 'GET':
        filtering_order = request.GET.get('filtering_order', request.session['filtering_order'])
        # HTML의 form 내부, GET방식을 통하여 들어오는 name=filtering_order값을 가져옴. None이면 세션값을 가져옴

        # 필터링 유지하기 위하여, 세션 방식 사용 - ajax같은 다른 방식이 있는데 현재로써는 어려움
        if filtering_order == "all":  # filtering, random output
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  # 현재 화면을 그대로 유지하여 새로고침
        elif filtering_order == "upper40":
            request.session['filtering_order'] = filtering_order  # 세션 저장
            list_data = TbUser.objects.filter(churn_proba__gte=40).order_by("?")
            # __gte는 이상이라는 뜻, 입력받은 값 이상을 출력(Greater Then or Equal)
        elif filtering_order == "upper60":
            request.session['filtering_order'] = filtering_order
            list_data = TbUser.objects.filter(churn_proba__gte=60).order_by("?")
        elif filtering_order == "potential":
            request.session['filtering_order'] = filtering_order
            list_data = TbUser.objects.filter(churn_proba_group="Potential").order_by("?")
        elif filtering_order == "high":
            request.session['filtering_order'] = filtering_order
            list_data = TbUser.objects.filter(churn_proba_group="High").order_by("?")
        elif filtering_order == "total":
            request.session['filtering_order'] = filtering_order
            list_data = list_data = TbUser.objects.all().order_by("?")
        else:
            filtering_order = "total"
            list_data = TbUser.objects.all().order_by("?")

        filtered_name_dict = {"all": "", 
                              "total": "전체 보기", 
                              "upper40": "이탈 확률 40% 이상", 
                              "upper60": "이탈 확률 60% 이상", 
                              "potential": "잠재 이탈자 그룹", 
                              "high": "고위험 그룹",
                              }  # 화면 표기용 dict 설정

        proba_avg = TbUser.objects.aggregate(Avg('churn_proba'))['churn_proba__avg']  
        # aggregate는 함수를 queryset에 적용하는 메소드, pandas의 apply/agg와 유사함
        # 장고는 메소드들을 불러오는 . 말고도, 이름을 불러오는 __ 도 자주 사용됨
        page = request.GET.get('page')
        lines, paginator, custom_range = pagination(list_data, page)  # 페이지 나누기 작업

        context = {"list_data": list_data, 
                   "lines": lines,  # paginator 결과
                   "paginator": paginator,  # paginator 데이터
                   "custom_range": custom_range,  # 페이지 길어지는 것 방지
                   "end_page": paginator.num_pages,  # 마지막 페이지 확인
                   "paginator_idx": paginator.num_pages - 2,  # 마지막 페이지 가까울 때 중복 출력 방지용 기준점
                   "filtering_order_name": filtered_name_dict[filtering_order],
                   "filtered_name": filtering_order,
                   "proba_avg": proba_avg,
                   }

        return render(request, 'list.html', context)


def customer_detail(request):  # 고객 ID를 통한 세부 고객 정보 페이지 단순 출력
    request.session['filtering_order'] = None

    list_data = TbUser.objects.all()  # 자동완성 기능 구현을 위한, 유저 정보 불러오기

    context = {"text": "먼저 고객을 검색하세요", 
               "c_id": None,
               "list_data": list_data,
               }

    return render(request, "detail.html", context)


def customer_detail_selected(request, customer_ids=0):  # 리스트 페이지 고객 ID를 링크를 통한 세부 고객 정보 출력
    request.session['filtering_order'] = None

    list_data = TbUser.objects.all()  # 자동완성 기능 구현을 위한, 유저 정보 불러오기
    data = TbUser.objects.filter(customer_id=customer_ids)  # 선택된 고객 아이디를 받아서 이에 해당되는 쿼리만 가져옴

    cltv_value = list(TbUser.objects.filter(customer_id=customer_ids).values())[0]['cltv']
    tr_value = list(TbContract.objects.filter(customer_id=customer_ids).values())[0]['total_revenue']
    tm_value = list(TbContract.objects.filter(customer_id=customer_ids).values())[0]['tenure_in_months']
    nod_value = list(TbService.objects.filter(customer_id=customer_ids).values())[0]['number_of_dependents']
    # .values()를 사용하면 쿼리의 결과가 ({column:value, ...}) 형식으로 출력됨
    # 이를 리스트로 변환하고, idx를 이용한 인덱싱 > dict에서 값을 불어오는 방식중 하나인 []로 호출

    suggestion_text = marketing_suggest(cltv_value, tr_value, tm_value, nod_value)  # 마케팅 제안을 위한 함수 호출

    context = {"text": suggestion_text, 
               "c_id": customer_ids, 
               "data": data,
               "list_data": list_data,
               }

    return render(request, "detail.html", context)


def customer_detail_search(request, customer_ids=0):  # 고객 정보 페이지의 검색창을 통한 세부 고객 정보 출력
    request.session['filtering_order'] = None
    
    checkpoint = request.GET.get("input_cs_id")
    if checkpoint == "":  # 검색창으로 아무것도 들어오지 않는 경우는 세부 페이지로 리다이렉트
        return redirect('customer-detail')

    else:
        list_data = TbUser.objects.all()
        data = TbUser.objects.filter(customer_id=checkpoint)

        if data.exists():  # data/검색 결과가 존재하는 경우에만 동작
            cltv_value = list(TbUser.objects.filter(customer_id=checkpoint).values())[0]['cltv']
            tr_value = list(TbContract.objects.filter(customer_id=checkpoint).values())[0]['total_revenue']
            tm_value = list(TbContract.objects.filter(customer_id=checkpoint).values())[0]['tenure_in_months']
            nod_value = list(TbService.objects.filter(customer_id=checkpoint).values())[0]['number_of_dependents']

            suggestion_text = marketing_suggest(cltv_value, tr_value, tm_value, nod_value)

            context = {"text": suggestion_text, 
                       "c_id": checkpoint, 
                       "data": data,
                       "list_data": list_data,
                       }
            return render(request, 'detail.html', context)

        else:  # 검색 결과가 없는 경우, 현재 페이지 유지
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def dashboard(request):  # 시각화
    request.session['filtering_order'] = None

    viewing_dict = {"user": "/static/images/category_user.png",  # 카테고리 변경을 위한 dict
                    "service": "/static/images/category_service.png", 
                    "contract": "/static/images/category_contract.png"
                    }

    viewing_key = request.GET.get('dropdown_select')

    if viewing_key is None:  # 최초 실행시에는 None이기 때문에, 이를 처리하기 위한 if문 추가
        viewing_key = 'user'
        viewing = viewing_dict["user"]  # "user" 대신 viewing_key 써도 상관 없음
    else:
        viewing = viewing_dict[viewing_key]

    context = {"now_view": viewing, }  # 기본 context 작성

    # 출력할 결과들에 대해서 내용을 리스트로/dict는 for문을 통하여 구성해도 되나, 우선 급한대로 노가다형 dict 구성
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

    if request.method == "GET":  # 최초 로딩시 불러올 화면
        return render(request, 'administrator.html')

    elif request.method == "POST":
        execute_order = request.POST.get('order')  # 버튼 누르는 것 확인, 현재는 확률 재계산만 가능
        if execute_order == 'recalc':  # 확률 재계산일 때 시행 
            column_name = ["Age", "Number of Dependents", "Satisfaction Score", "Tech services", "Streaming services",
                           "Combined Product", "Tenure in Months", "Monthly Charge", "Total Revenue", "Membership_None",
                           "Membership_Offer A", "Membership_Offer B", "Membership_Offer C", "Membership_Offer D", "Membership_Offer E",
                           "Contract_Month-to-Month", "Contract_One Year", "Contract_Two Year",]

            queryset = TbUser.objects.all()

            # 여러 테이블에 나누어져 있어서, 각 테이블에 해당되는 컬럼을 별도로 체크, 이를 update 형식으로 dict에 추가
            # name = Max(column) 식으로 하면, column__max 로 출력되는 dict의 key가 지정된 name으로 변환된다.
            # join 기능인 select_related써서 접근해도 되지만, Max나 Min 안에 들어갈 컬럼명이 너무 길어져서 보류
            mmdict = TbUser.objects.aggregate(
                            age_max=Max('age'), age_min=Min('age'), 
                            satisfaction_score_max=Max('satisfaction_score'), satisfaction_score_min=Min('satisfaction_score')
                            )
            mmdict.update(TbService.objects.aggregate(
                                number_of_dependents_max=Max('number_of_dependents'), number_of_dependents_min=Min('number_of_dependents'), 
                                tech_services_max=Max('tech_services'), tech_services_min=Min('tech_services'),
                                streaming_services_max=Max('streaming_services'), streaming_services_min=Min('streaming_services'), 
                                combined_product_max=Max('combined_product'), combined_product_min=Min('combined_product'))
                          )
            mmdict.update(TbContract.objects.aggregate(
                                tenure_in_months_max=Max('tenure_in_months'), tenure_in_months_min=Min('tenure_in_months'), 
                                monthly_charge_max=Max('monthly_charge'), monthly_charge_min=Min('monthly_charge'), 
                                total_revenue_max=Max('total_revenue'), total_revenue_min=Min('total_revenue'))
                          )

            for i in range(len(queryset)):
                proba_list = single_row_predict(queryset[i], mmdict)

                predict_data = pd.DataFrame(data=np.array(proba_list).reshape(1, -1), columns=column_name)  # predict proba는 (-1, 1) shape를 요구함
                predict_result = TelcoDefenceConfig.mlmodels.predict_proba(predict_data)[0][1] * 100  # 1, Churn할 확률을 계산

                target_row = TbUser.objects.get(customer_id=queryset[i].customer_id)  # 계산한 해당 id를 타겟으로 지정

                target_row.churn_proba = round(predict_result, 4)  # 연산 결과를 타켓 row의 churn_proba에 입력

                if predict_result >= 60:  # 그룹 지정
                    target_row.churn_proba_group = 'High'
                elif predict_result >= 40:
                    target_row.churn_proba_group = 'Potential'
                else:
                    target_row.churn_proba_group = 'Stable'

                target_row.save()  # 입력한 결과를 DB에 저장
        return redirect('administration_page')
