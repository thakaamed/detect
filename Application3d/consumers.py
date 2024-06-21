# import json
# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# import os

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#         self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'You are now connected!',
#         }))


# class FileUploadConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         chunk = data.get('chunk', None)
#         session_id = data.get('session_id', None)

#         if chunk and session_id:
#             await self.process_chunk(session_id, chunk)

#     async def process_chunk(self, session_id, chunk):
#         # Save the chunk to a temporary file
#         temp_file_path = f'temp_files/{session_id}.part'
#         with open(temp_file_path, 'ab') as temp_file:
#             temp_file.write(chunk)
