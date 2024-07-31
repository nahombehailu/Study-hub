from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerilizer

@api_view(['GET'])
def getRoute(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serilizer=RoomSerilizer(rooms,many=True)
    return Response(serilizer.data)

@api_view(['GET'])
def getRoom(request,pk):
    room=Room.objects.get(id=pk)
    serilizer=RoomSerilizer(room,many=False)
    return Response(serilizer.data)