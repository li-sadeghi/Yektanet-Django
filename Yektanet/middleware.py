from advertiser_mangement.models import View, Ad

class ViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for ad in Ad.objects.all():
            new_view = View(ad=ad, viewer_ip=request.META)
            new_view.save()
            
        response = self.get_response(request)

        return response
