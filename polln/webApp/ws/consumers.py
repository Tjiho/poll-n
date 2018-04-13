from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from webApp.models import Question,Anonym_user,Answer,User
from channels.auth import get_user

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
        user = self.get_user(self.scope)

        if poll and  self.poll \
                and poll['question'].token == self.poll['question'].token \
                and 'type' in text_data_json:
            if text_data_json["type"] == "new_answer":
                if (poll["admin"]   or user.is_authenticated
                                    or poll["question"].annonymous_can_add_answer)\
                                    and 'message' in text_data_json:

                    
                    message = text_data_json['message']
                    if message:
                        answer = Answer.objects.create(
                            title = message,
                            question = poll["question"]
                        )

                        answer.change_state_user(user.pk, user.is_login(), True, poll["admin"])

                        # Send message to room group
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'new_answer',
                                'message': message,
                                'pk': answer.pk,
                                'username': str(user),
                                'percentage': answer.percentage,
                                'user_pk':user.pk
                            }
                        )
            elif text_data_json["type"] == "new_title":
                if poll["admin"] and 'message' in text_data_json:
                    message = text_data_json['message']
                    if message:
                        poll["question"].title = message
                        poll["question"].save()
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            text_data_json
                        )
            elif text_data_json["type"] == "new_description":
                if poll["admin"] and 'message' in text_data_json:
                    message = text_data_json['message']
                    if message:
                        poll["question"].description = message
                        poll["question"].save()
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            text_data_json
                        )
            elif text_data_json["type"] == "new_check_answer" :
                if 'answer' in text_data_json \
                and 'checked' in text_data_json:

                    answer = Answer.objects.get(pk=text_data_json["answer"])
                    if answer.change_state_user(user.pk, user.is_login(), text_data_json['checked'], poll["admin"]):
                        self.send_Room_check_answer(
                            user.username,
                            user.is_login(),
                            answer,
                            user.pk,
                            text_data_json['checked']
                        )

            elif text_data_json["type"] == "new_option":
                 if poll["admin"] and 'message' in text_data_json and 'value' in text_data_json:
                    message = text_data_json['message']
                    if message == "annonymous_can_add_answer":
                        poll["question"].annonymous_can_add_answer = text_data_json['value']
                    elif message == "annonymous_can_answer":
                        poll["question"].annonymous_can_answer = text_data_json['value']
                    
                    poll["question"].save()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        text_data_json
                    )

            elif text_data_json["type"] == "delete_answer":
                if poll["admin"] and 'answer' in text_data_json:
                    answer = Answer.objects.get(pk=text_data_json["answer"])
                    answer.delete()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        text_data_json
                    )

    def get_user(self,scope):
        user = get_user(self.scope)
        if user.is_authenticated:
            print("--- plop ---")
            return user
        elif self.scope["session"] and self.scope["session"]["user_anonym"]:
            user_pk = self.scope["session"]["user_anonym"]
            anonym = Anonym_user.objects.get(pk=user_pk)
            return anonym
        else:
            print("--- plaf ---")
            return False

                        
    def send_Room_check_answer(self,username,is_login,answer,user_pk,state):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_check_answer',
                'username': username,
                'is_login': is_login,
                'answer': answer.pk,
                'user_pk': user_pk,
                'state': state,
                'number_views': len(answer.question.participant),
                'number_vote': len(answer.question.real_participant),
                'number_accounts': len(answer.question.connected_participant.all()),
                'percentage':answer.percentage
            }
        )


                


    # ------------------- Receive message from room group -------------------


    def new_answer(self, event):
        # Send message to WebSocket
       self.send(text_data=json.dumps(event))

    def new_title(self,event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':  message,
            'type':     'new_title'
        }))
    
    def new_description(self,event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':  message,
            'type':     'new_description'
        }))

    def new_check_answer(self,event):
        self.send(text_data=json.dumps(event))
    
    def new_option(self,event):
        self.send(text_data=json.dumps(event))

    def delete_answer(self,event):
        self.send(text_data=json.dumps(event))
        