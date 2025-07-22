from django.http import JsonResponse
from .models import UserToken

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return JsonResponse({"error":"Token missing"},status=401)
        
        try:
            user_token = UserToken.objects.get(token=token)
            request.user = user_token.user
        except UserToken.DoesNotExist:
            return JsonResponse({"error":"Invalid token"},status=401)
        
        return view_func(request,*args,**kwargs)
    
    return wrapper


