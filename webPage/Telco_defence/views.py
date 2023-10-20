from django.shortcuts import render, redirect
from .models import TbUser, TbContract, TbService
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .module.create_functions import pagination, customer_create


# Create your views here.
def test(request):  # 읽기 테스트, paginator 추가(23.10.17~18)
    # testing_point = TbUser.objects.all()
    testing_point = TbUser.objects.filter(satisfaction_score=1).order_by('customer_id')
    # testing_point = TbUser.objects.filter(customer_id='0004-TLHLJ').select_related('tbcontract').order_by('customer_id')
    # testing_point = TbUser.objects.filter(customer_id='0004-TLHLJ')
    # testing_point = TbUser.objects.filter(customer_id='1')

    # print(testing_point.query)  # SQL 확인용
    page = request.GET.get('page')
    lines, paginator, custom_range = pagination(testing_point, page)

    context = {"testing_point": testing_point, 
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
        print(word)
        return redirect('itt_a')


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
    pass


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
'''


def main_page_render(request):  # 시작시 보여지는 메인페이지 렌더링
    return render(request, 'home.html')


def customer_list(request):  # 전체 고객 리스트 출력
    if request.method == 'GET':
        list_data = TbUser.objects.all()

        page = request.GET.get('page')
        lines, paginator, custom_range = pagination(list_data, page)

        context = {"list_data": list_data, 
                   "lines": lines,  # paginator 결과
                   "paginator": paginator,  # paginator 데이터
                   "custom_range": custom_range,  # 페이지 길어지는 것 방지
                   "end_page": paginator.num_pages,  # 마지막 페이지 확인
                   "paginator_idx": paginator.num_pages - 2,  # 마지막 페이지 가까울 때 중복 출력 방지용 기준점
                   }

        return render(request, 'list.html', context)

    # if request.method == 'POST':


def customer_detail(request, customer_ids=None):  # 고객 ID를 통한 세부 고객 정보 출력
    if request.method == "GET":
        if customer_ids is None:
            c_id = None
        else:
            c_id = customer_ids
        data = TbUser.objects.filter(customer_id=c_id)

        context = {"text": "This is marketing recommand", 
                   "c_id": c_id, 
                   "data": data}

        return render(request, 'detail.html', context)

    elif request.method == "POST":
        c_id = request.POST.get('input_cs_id')

        if c_id == "":
            return redirect('customer-detail')
        else:
            print(c_id, type(c_id))
            data = TbUser.objects.filter(customer_id=c_id)

            context = {"text": "This is marketing recommand", 
                       "c_id": c_id, 
                       "data": data}

            print(context["c_id"])
            return render(request, 'detail.html', context)


def dashboard(request):  # 시각화
    viewing_dict = {"user": "사용자 정보", "service": "서비스 정보", "contract": "요금제 정보"}
    viewing_key = request.POST.get('dropdown_select')

    if viewing_key is None:
        viewing = viewing_dict['user']
    else:
        viewing = viewing_dict[viewing_key]

    print(viewing)
    context = {"now_view": viewing, }
    return render(request, 'dashboard.html', context)
