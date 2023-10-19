# 아이디 생성
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
    except PageNotAnInteger:
        page = 1
        lines = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        lines = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return lines, paginator, custom_range


# 데이터 저장 - DB 연동 추가(Insert into)
def customer_create(request):
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
