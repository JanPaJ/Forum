from re import search
from main.models import Post


def searchFunction(request):
    posts = Post.objects.all()
    search_context = {}

    if "search" in request.GET:
        query = request.GET.get("q")
        # wybieranie wyników
        search_box = request.GET.get("search-box")
        if search_box == "Descriptions":
            objects = posts.filter(content__icontains = query)
        else:
            objects = posts.filter(title__icontains = query)

        search_context = {
            "objects":objects,
            "query": query,
    }

    return search_context