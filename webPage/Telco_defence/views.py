from django.shortcuts import render, redirect
from .models import TbUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def test(request):
    # testing_point = TbUser.objects.all()
    testing_point = TbUser.objects.filter(satisfaction_score=1).order_by('customer_id')
    # testing_point = TbUser.objects.filter(customer_id='0004-TLHLJ')

    page = request.GET.get('page')
    paginator = Paginator(testing_point, 20)  # 페이지 나누기 추가, (object_list, per_page)
    # lines = paginator.page(page)
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

    context = {"testing_point": testing_point, 
               "lines": lines, 
               "paginator": paginator, 
               "custom_range": custom_range,
               }
    # page_num = request.GET.get('page') # 페이지 번호 가져오기
    # testing_point_idx = paginator.get_page(page_num) # 페이지 인덱싱
    return render(request, 'test.html', context)


def inputtest(request):
    if request.method == 'GET':
        return render(request, 'inputtest.html')
    else:
        word = request.POST.get('testing')
        print(word)
        return redirect('itt_a')
