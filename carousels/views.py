from django.http    import JsonResponse
from django.views   import View 
from carousels.models import Carousel


class CarourselView(View) :
    def get(self,requset) :
        carousel_queryset = Carousel.objects.values()

        result = []

        for c in carousel_queryset :
            result.append({
                "id" : c["id"],
                "tag" : c["tags"],
                "image_url" : c["image_url"],
                "url_by_click" : c["url_to"]
            })
        
        return JsonResponse({"result" : result})
