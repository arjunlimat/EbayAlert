from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer

@api_view(['POST'])
def create_alert(request):
    serializer = AlertSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

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
