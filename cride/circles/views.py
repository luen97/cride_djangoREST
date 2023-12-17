"""Circle views"""

from django.http import HttpResponse, JsonResponse
from cride.circles.models import Circle

def list_circles(request):
    """List circles"""

    circles = Circle.objects.all()
    public = circles.filter(is_public=True)

    data = []

    for circle in public:
        data.append({
            'name':circle.name,
            'slug_name':circle.slug_name,
            'rides_taken':circle.rides_taken,
            'rides_offered':circle.rides_offered,
            'members_limit':circle.members_limit

        })
    return JsonResponse(data, safe=False)