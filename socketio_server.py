import socketio
from asgiref.sync import sync_to_async
import json
import django
import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
django_app = get_wsgi_application()

from src.users_app.services.users_service import UserService


socket_io_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
# TODO logger
app = socketio.ASGIApp(socket_io_server)


class GameNamespace(socketio.AsyncNamespace):
    """
    Class-based namespace for socket connection between two users
    in the contra_in_browser game.
    """

    # def __init__(self):
    #     self.sid_user_dictionary = {}
    sid_user_dictionary = {}
    sid_rooms_dict = {}


    async def on_connect(self, sid, environ) -> None:
        """
        Connection event. Checks if user authentication data is valid
        and returns a token for creating a room.

        Args:
            sid (str): Session identifier
            environ (dict): Environment dictionary
            data: Additional data from the connection

        Returns:
            None
        """
        result = await sync_to_async(UserService.check_if_token_is_correct)\
                                    (environ.get('HTTP_AUTHORIZATION'))
        if result.user_id: 
            self.sid_user_dictionary[sid] = result.user_id
        print('***')
        print(self.sid_user_dictionary)
        print('***')
        await self.emit('authentication_status', data=result.dict(),\
                                                room=sid, \
                                                namespace='/game')


    async def on_create_room(self, sid, data=None) -> None:
        """
        Creating room command. Receives a token (obtained from the connection)
        and creates a room.

        Args:
            sid (str): Session identifier
            data (dict): Data containing the room token

        Returns:
            None
        """
        user_id = self.sid_user_dictionary[sid]
        room_token = await sync_to_async(UserService.generate_enter_the_room_token)(user_id)
        room_token_message = {'room_token': room_token}

        await self.enter_room(sid, room_token)
        self.sid_rooms_dict[sid] = room_token
        await self.emit('connection_with_created_room', data=room_token_message,\
                                                room=sid, \
                                                namespace='/game')

        

    async def on_send_message_to_game_partner(self, sid, data):
        # print(data)
        current_room = self.sid_rooms_dict[sid]
        await self.emit('receive_message_from_room', data=data,
                                                    room=current_room,
                                                    skip_sid=sid,
                                                    namespace='/game')


    async def on_join_room(self, sid, data: dict) -> None:
        """
        Function that joins a user to a room using a room token.
        This token is received from the game partner 
        (in other way, not throw contra_in_browser) and used for connection.

        Args:
            sid (str): Session identifier
            data (dict): Data containing the room token in JSON format

        Returns:
            None
        """

        dictionary = json.loads(data)
        
        await self.enter_room(sid, dictionary['room_token'])
        test_message_dict = {'message': 'users joined the room!'}

        self.sid_rooms_dict[sid] = dictionary['room_token']
        
        await self.emit('test_message_for_certain_room', data=test_message_dict,\
                                                room=dictionary['room_token'], \
                                                namespace='/game')
    


    async def on_disconnect(self, sid) -> None:
        """
        Disconnection function.

        Args:
            sid (str): Socket ID

        Returns:
            None
        """
        print(f'Disconnected: {sid}')



socket_io_server.register_namespace(GameNamespace('/game')) # namespace registration


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)