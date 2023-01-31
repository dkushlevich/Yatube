from django.core.paginator import Paginator


def paginator_for_posts(request, posts, page_num):
    paginator = Paginator(posts, page_num)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
