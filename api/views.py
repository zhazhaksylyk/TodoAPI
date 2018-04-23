from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from api.models import Todo
from api.serializers import TodoSerializer



@csrf_exempt
def todo_list(request):
    if(request.method == "GET"):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif(request.method == "POST"):
        todoToAdd = JSONParser().parse(request)
        serializer = TodoSerializer(data=todoToAdd)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def todo_detail(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
    if(request.method == "GET"):
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)
    elif(request.method == "PUT"):
        curTodo = JSONParser().parse(request)
        serializer = TodoSerializer(todo, curTodo)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
    elif(request.method == "DELETE"):
        todo.delete()
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)

