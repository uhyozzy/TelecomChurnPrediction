# 고객 아이디 생성
def create_id():
    """ ## Create new id
    ### Input
    - None

    ### Output
    - Length 10 String
    """
    import random
    import string

    # id 숫자 부분 구현
    number = "{0:04d}".format(random.randint(0000, 10000))  # 임의의 1~4자리 숫자, 빈칸은 0으로 채움

    # id 영어 부분 구현
    leng = 5  # 최대 길이 5
    string_pool = string.ascii_uppercase  # 아스키 코드에서 대문자만 차용
    temp = ""  # 임시 문자열
    for i in range(leng):
        temp += random.choice(string_pool)  # 5자리가 될 때까지 문자열 추가
    strings = temp  # 문자열 저장

    result = number + "-" + strings  # 10자리 문자열 id 생성
    return result


# 다량의 데이터 페이지 나누기(django paginator)
def pagination(inputpage, page):
    """ ## Pagination function

    ### Input
    > 2 Input parameter need
    - objects : django queryset
    - page : Getting page(request.GET.get('page'))

    ### Output
    > 3 Output variable need
    - lines : page object
    - paginator : pagination, 20 contents per each page 
    - custom_range : -2 ~ +2 page range 
    """
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

    paginator = Paginator(inputpage, 20)  # 페이지 나누기 추가, (object_list, per_page)

    try:
        lines = paginator.page(page)
    except PageNotAnInteger:  # page가 수치가 아닐때 ==> 페이지를 나눌 수 없어 None
        page = 1
        lines = paginator.page(page)
    except EmptyPage:  # 페이지 번호를 넘길 때(최대치보다 높은 페이지 수)
        page = paginator.num_pages
        lines = paginator.page(page)

    left_index = (int(page) - 2)  # 좌측 인덱싱 범위 설정
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)  # 우측 인덱싱 범위 설정
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return lines, paginator, custom_range


# 대시보드 그래프 그리기
def dashboard_management(selection, queryset):
    import plotly.express as px  # 이건 필요없나? 지우고 해봐야겠다.
    import kaleido

    import pandas as pd
    import numpy as np

    if selection == 'user':
        from ..module.Dashboard import user_chart_corr, user_chart_stat
        x_cols = ['Age', 'Membership', 'Satisfaction Score', 'CLTV', 'Churn Value']
        target_df = pd.DataFrame(list(queryset), columns=x_cols)
        user_chart_stat(target_df)
        user_chart_corr(target_df)

    elif selection == 'service':
        from ..module.Dashboard import service_chart_corr, service_chart_stat
        x_cols = ['Tech services', 'Streaming services', 'Number of Dependents', 'Combined Product', 'Churn Value']
        target_df = pd.DataFrame(list(queryset), columns=x_cols)
        service_chart_stat(target_df)
        service_chart_corr(target_df)

    elif selection == 'contract':
        from ..module.Dashboard import bill_chart_corr, bill_chart_stat
        x_cols = ['Contract', 'Tenure in Months', 'Monthly Charge', 'Total Revenue', 'Churn Value']
        target_df = pd.DataFrame(list(queryset), columns=x_cols)
        bill_chart_stat(target_df)
        bill_chart_corr(target_df)


# 마케팅 제안
def marketing_suggest(CLTV, total_revenue, tenure_months, num_dependents):
    """ ## Input
    - ['CLTV']: Amount of total expected value per person that might contribute in the future.
    - ['total_revenue']: The total annual earnings from each customer.
    - ['tenure_months']: The duration for which each customer has retained their contracts.
    - ['num_dependent']: The number of children in family customers.

    ## Output
    - String
    """

    if CLTV >= 6000 and total_revenue >= 10000:
        return "CLTV 높은 고가치 기업 고객님 입니다. [결합 할인 + 요금할인(20%)] 제안 가능합니다."
    elif 5000 <= CLTV < 6000 and total_revenue >= 10000:
        return "CLTV 높은 고가치 기업 고객님 입니다. [결합 할인 + 요금할인(18%)] 제안 가능합니다."
    elif 4000 <= CLTV < 5000 and 6000 >= total_revenue < 10000:
        return "CLTV 높은 고가치 기업 고객님 입니다. [결합 할인 + 요금할인(15%)] 제안 가능합니다."
    elif CLTV >= 5000 and tenure_months >= 60 and num_dependents > 0:
        return "CLTV 높은 고가치 개인 고객님 입니다. [결합 할인 + 요금할인(10%)] 제안 가능합니다."
    elif 5000 <= CLTV < 6000 and 4500 <= total_revenue < 6000:
        return "CLTV 중간 가치 기업 고객님(잠재적 이탈 고객층) 입니다. [요금 할인(13%)] 제안 가능합니다."
    elif 4001 <= CLTV < 5000 and 2000 <= total_revenue < 4500:
        return "CLTV 중간 가치 기업 고객님(잠재적 이탈 고객층) 입니다. [요금 할인(10%)] 제안 가능합니다."
    elif 4000 <= CLTV < 6000 and 36 <= tenure_months < 60:
        return "CLTV 중간 가치 개인 고객님(잠재적 이탈 고객층) 입니다. [할인 혜택 or 업그레이드 or 맞춤형] 제안 가능합니다."
    elif 2000 <= CLTV < 4000 and total_revenue >= 6000:
        return "CLTV 낮지만 수익 가치가 높은 기업 고객님 입니다. [요금 할인(15%)] 제안 가능합니다."
    elif 2000 <= CLTV < 4000 and 4000 <= total_revenue < 6000:
        return "CLTV 낮지만 수익이 중간 가치인 기업 고객님 입니다. [요금 할인(10%)] 제안 가능합니다."
    elif CLTV > 4000 and 24 <= tenure_months < 36:
        return "CLTV 낮은 저가치 개인 고객님 입니다. [할인 혜택 or 업그레이드 or 맞춤형] 제안 가능합니다."
    # 경우의 수 추가 부분 
    elif CLTV <= 4000 and tenure_months < 24:
        return "CLTV 낮은 저가치 개인 고객님 입니다. [업그레이드 or 맞춤형] 제안 가능합니다."
    elif 2000 <= CLTV < 4000 and tenure_months < 24:
        return "CLTV 낮은 저가치 개인 고객님 입니다. 제안할 마케팅 제안이 없습니다."        
    else:
        return "제안할 마케팅 제안이 없습니다."  # 231025, 마케팅 추가 수정


# 데이터 저장 - DB 연동 추가(Insert into)
def customer_create(request):
    """ ## Customer Create function
    사용할 지 모르는 상태. 일단 기능 구현 완료(23.10.20)
    """
    from ..models import TbContract, TbService, TbUser

    customer_ids = create_id()
    if TbUser.objects.filter(customer_id=customer_ids).exists():
        # id 중복여부 확인
        customer_ids = create_id()

    new_customer_info_u = TbUser()
    new_customer_info_c = TbContract()
    new_customer_info_s = TbService()

    new_customer_info_u.customer_id = customer_ids
    new_customer_info_u.age = request.POST.get('age')
    new_customer_info_u.satisfaction_score = request.POST.get('satisfaction_score')
    new_customer_info_u.membership = request.POST.get('membership')
    new_customer_info_u.churn_value = request.POST.get('churn_value')
    # new_customer_info_u.save()
    print("customer_id", new_customer_info_u.customer_id)
    print("age", new_customer_info_u.age)
    print("satisfaction_score", new_customer_info_u.satisfaction_score)
    print("membership", new_customer_info_u.membership)
    print("churn_value", new_customer_info_u.churn_value)

    new_customer_info_c.customer_id = new_customer_info_u.customer_id
    new_customer_info_c.contract = request.POST.get('contract')
    new_customer_info_c.tenure_in_months = 1
    new_customer_info_c.monthly_charge = request.POST.get('monthly_charge')
    new_customer_info_c.total_revenue = request.POST.get('total_revenue')
    # new_customer_info_c.save()
    print("customer_id", new_customer_info_c.customer_id)
    print("contract", new_customer_info_c.contract)
    print("tenure_in_months", new_customer_info_c.tenure_in_months)
    print("monthly_charge", new_customer_info_c.monthly_charge)
    print("total_revenue", new_customer_info_c.total_revenue)

    new_customer_info_s.customer_id = new_customer_info_u.customer_id
    new_customer_info_s.tech_services = request.POST.get('tech_services')
    new_customer_info_s.streaming_services = request.POST.get('streaming_services')
    new_customer_info_s.combined_product = request.POST.get('combined_product')
    new_customer_info_s.number_of_dependents = request.POST.get('number_of_dependents')
    # new_customer_info_s.save()
    print("customer_id", new_customer_info_s.customer_id)
    print("tech_services", new_customer_info_s.tech_services)
    print("streaming_services", new_customer_info_s.streaming_services)
    print("combined_product", new_customer_info_s.combined_product)
    print("number_of_dependents", new_customer_info_s.number_of_dependents)


# 데이터 삭제 - DB 연동 삭제(Delete from)
def customer_delete():
    pass


# 데이터 수정 - DB 연동 수정(Update set)
def customer_edit():
    pass
