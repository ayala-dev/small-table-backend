from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# --- CREATE ---
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')

            if not all([username, email, password]):
                return JsonResponse({'error': 'Username, email, and password are required.'}, status=400)

            # --- DB LOGIC (Commented Out) ---
            # user = User.objects.create_user(username=username, email=email, password=password)
            # if hasattr(user, 'phone') and phone:
            #     user.phone = phone
            #     user.save()
            
            return JsonResponse({
                'status': 'success (simulation)',
                'message': f"User '{username}' would be created."
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST only.'}, status=405)

# --- READ (All) ---
@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        # --- DB LOGIC (Commented Out) ---
        # users = User.objects.all()
        # data = list(users.values('id', 'username', 'email', 'phone'))
        # return JsonResponse(data, safe=False)
        
        return JsonResponse([
            {'id': 1, 'username': 'simulated_user_1', 'email': 'user1@example.com', 'phone': '123'},
            {'id': 2, 'username': 'simulated_user_2', 'email': 'user2@example.com', 'phone': '456'}
        ], safe=False, status=200)
    return JsonResponse({'error': 'GET only.'}, status=405)

# --- READ (By ID) ---
@csrf_exempt
def get_user_by_id(request, id):
    if request.method == 'GET':
        # --- DB LOGIC (Commented Out) ---
        # try:
        #     user = User.objects.get(pk=id)
        #     data = {'id': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}
        #     return JsonResponse(data)
        # except User.DoesNotExist:
        #     return JsonResponse({'error': 'User not found.'}, status=404)
        
        return JsonResponse({
            'id': id, 'username': f'simulated_user_{id}', 'email': f'user{id}@example.com', 'phone': '789'
        }, status=200)
    return JsonResponse({'error': 'GET only.'}, status=405)

# --- UPDATE ---
@csrf_exempt
def edit_user(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required.'}, status=400)

            # --- DB LOGIC (Commented Out) ---
            # user = User.objects.get(pk=user_id)
            # if 'username' in data: user.username = data['username']
            # if 'email' in data: user.email = data['email']
            # if 'phone' in data: user.phone = data['phone']
            # user.save()

            return JsonResponse({'status': 'success (simulation)', 'message': f"User {user_id} would be updated."})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'PUT only.'}, status=405)

# --- DELETE ---
@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required.'}, status=400)

            # --- DB LOGIC (Commented Out) ---
            # user = User.objects.get(pk=user_id)
            # user.delete()

            return JsonResponse({'status': 'success (simulation)', 'message': f"User {user_id} would be deleted."})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'DELETE only.'}, status=405)
