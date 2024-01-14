from django.http import JsonResponse

from .models import Item


def search_suggestion(request):
    query = request.GET.get("query", "")
    suggestions = Item.objects.filter(name__icontains=query).values("id", "name")
    suggestions_list = [
        {"id": suggestion["id"], "name": suggestion["name"]}
        for suggestion in suggestions
    ]
    return JsonResponse(suggestions_list, safe=False)
