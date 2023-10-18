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
