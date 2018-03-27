from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from webApp.models import Question,Anonym_user,Option,Answer

import json



def getPoll(token):
    if Question.objects.filter(token=token).exists():
        admin = False
        question = Question.objects.get(token=token)
    elif Question.objects.filter(token_admin=token).exists():
        admin = True
        question = Question.objects.get(token_admin=token)
    else:
        return False

    return {'question':question,'admin':admin}




class PollAnswerConsumer(WebsocketConsumer):

    

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['key']
        self.poll = getPoll(self.room_name)
        if self.poll:
            self.room_group_name = 'poll_%s' % self.poll['question'].token
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        token = self.scope['url_route']['kwargs']['key']
        poll = getPoll(token)
        text_data_json = json.loads(text_data)

        if poll and  self.poll \
                and poll['question'].token == self.poll['question'].token \
                and 'type' in text_data_json \
                and 'message' in text_data_json:

            if text_data_json["type"] == "new_answer":
                if poll["admin"] or self.scope["user"].is_authenticated:

                    
                    message = text_data_json['message']
                    if message:
                        answer = Answer.objects.create(
                            title = message,
                            question = poll["question"]
                        )
                        # Send message to room group
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'new_answer',
                                'message': message
                            }
                        )
            elif text_data_json["type"] == "new_title":
                if poll["admin"]:
                    message = text_data_json['message']
                    if message:
                        poll["question"].title = message
                        #poll["question"].objects.save()
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'new_title',
                                'message': message
                            }
                        )
            elif text_data_json["type"] == "new_description":
                if poll["admin"]:
                    message = text_data_json['message']
                    if message:
                        poll["question"].description = message
                        #poll["question"].objects.save()
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'new_description',
                                'message': message
                            }
                        )


    # Receive message from room group
    def new_answer(self, event):
        message = event['message']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'new_answer'
        }))

    def new_title(self,event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'new_title'
        }))
    
    def new_description(self,event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'new_description'
        }))