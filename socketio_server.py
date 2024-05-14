import socketio

import socketio
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.handlers.asgi import ASGIRequest
from asgiref.sync import sync_to_async
import json
import django
import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()
django_app = get_wsgi_application()
from src.users_app.services.users_service import UserService



socket_io_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = socketio.ASGIApp(socket_io_server)

rooms = {}

class GameNamespace(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ, *data):
        result = await sync_to_async(UserService.check_if_token_is_correct)\
                                    (environ.get('HTTP_AUTHORIZATION'))
        await self.emit('authentication_status', data=result.dict(),\
                                                room=sid, \
                                                namespace='/game')
        
    async def on_create_room(self, sid, data):
        print('---creating---room---')
        print(sid)
        print(data['room_token'])
        print('---------------------')
        # rooms[room_name] = [sid]
        # await self.enter_room(sid, room_name)
        await self.enter_room(sid, data['room_token'])
        print(f"Client {sid} created room with {data}.")
        await self.emit('connection_with_created_room', data=data,\
                                                room=sid, \
                                                namespace='/game')

        

    async def on_join_room(self, sid, data):

        print('--->you have triggered JOIN---ROOM<---s')

        # print(data['room_token'])
        dictionary = json.loads(data)

        await self.enter_room(sid, dictionary['room_token'])

        print(f"Client {sid} have joined the room {dictionary['room_token']}.")
        print('=======================================')

        await self.emit('test_message_for_certain_room', data=data,\
                                                room=dictionary['room_token'], \
                                                namespace='/game')
    


    async def on_disconnect(self, sid):
        print(f'Disconnected: {sid}')






socket_io_server.register_namespace(GameNamespace('/game'))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)