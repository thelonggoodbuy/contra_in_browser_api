# myapp/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import socketio

sio = socketio.Server()

@sio.event
async def connect(sid, environ):
    print('Client connected', sid)

@sio.event
async def message(sid, data):
    await sio.emit('response', data)

@sio.event
async def disconnect(sid):
    print('Client disconnected', sid)

@csrf_exempt
async def websocket(request):
    return await sio.handle_request(request)
