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
               "lines": lines, 
               "paginator": paginator, 
               "custom_range": custom_range,
               "end_page": paginator.num_pages,
               "paginator_idx": paginator.num_pages - 2,
               }

    return render(request, 'index.html', context)


def inputtest(request):  # 입력 테스트(23.10.17~18)
    if request.method == 'GET':
        return render(request, 'inputtest.html')
    else:
        word = request.POST.get('testing')
        print(word)
        return redirect('itt_a')


def savetest(request):  # 신규 생성 및 DB 반영 테스트 진행(23.10.18)
    if request.method == 'GET':
        return render(request, 'savetest.html')
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
    pass

def customer_list(request):  # 전체 고객 리스트 출력
    pass

def customer_detail(request):  # 고객 ID를 통한 세부 고객 정보 출력
    pass

def new_customer(request):  # 신규 고객 정보 입력
    # GET, POST 나누어야 함
    # save 사용
    pass

def edit_customer(request):  # 기존 고객 정보 수정
    # GET, POST 나누어야 함
    pass

def dashboard_1(request):  # 시각화
    pass

def dashboard_2(request):
    pass