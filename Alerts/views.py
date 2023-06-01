from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer
from django.shortcuts import render
from rest_framework.request import Request
from django.http import HttpResponse
from django.core.mail import send_mail

def create_alert(request):
    if request.method == 'POST':
        serializer = AlertSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            # Send email to the user
            search_phrase = request.POST.get('search_phrase')
            email = request.POST.get('email')
            frequency = request.POST.get('frequency')
            
            return HttpResponse("Alert created successfully!")
        return Response(serializer.errors, status=400)
    else:
        if request.method == 'GET':
            return render(request, 'create_alert.html')
        else:
            return HttpResponse("Method not allowed.", status=405)

@api_view(['GET'])
def alert_list(request):
    alerts = Alert.objects.all()
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_alert(request, alert_id):
    alert = get_object_or_404(Alert, pk=alert_id)
    serializer = AlertSerializer(alert)
    return Response(serializer.data)

@api_view(['PUT'])
def update_alert(request, alert_id):
    alert = get_object_or_404(Alert, pk=alert_id)
    serializer = AlertSerializer(alert, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, pk=alert_id)
    alert.delete()
    return Response(status=204)
