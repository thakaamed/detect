from Application.models import *
from User.models import *
from django.http import JsonResponse

def dashboard_update_user_infos(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            profile = Profile.objects.get(user=user)
            profile.phone = phone
            user.save()
            profile.save()
            return JsonResponse({'message': 'User infos updated'},status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'User or profile not found'}, status=404)
        except Exception as e:
            # Diğer hataları loglayabilir veya özel bir mesaj döndürebilirsiniz
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)