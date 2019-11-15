from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from classroom.models import Teacher
import json

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    current_user_object = {}
    current_user_json = {}
    quiz_question_set = []
    is_teacher = False
    game_click = 0
    game_click_goal = 10

    def whoami(self, data):
        user = data['user']
        self.current_user_object = User.objects.filter(username=user)[0]
        self.current_user_json = self.user_to_json(self.current_user_object)
        teacher_obj = Teacher.objects.filter(user_id=self.current_user_object.id)
        if teacher_obj:
            self.is_teacher = True

    def new_message(self, data):
        content = data['message']
        content = {
            'command': 'new_message',
            'message': {
                'author': self.current_user_json,
                'content': content
            }
        }
        return self.send_action(content)

    def start_quiz(self, data):
        self.quiz_question_set = data['questions']
        quiz_mode = data['mode']
        content = {
            'command': 'start_quiz',
            'mode': quiz_mode,
            'questions': data['questions']

        }
        return self.send_action(content)

    def send_reply(self, data):
        content = {
            'command': 'send_reply',
            'data': {
                'user': self.current_user_json,
                'data': data['data']
            }
        }
        return self.send_action(content)

    def get_answer(self, data):
        content = {
            'command': 'get_answer',
        }
        return self.send_action(content)

    def next_question(self, data):
        content = {
            'command': 'next_question',
            'next_question': data['next_question']
        }
        return self.send_action(content)

    def end_quiz(self, data):
        content = {
            'command': 'end_quiz',
        }
        return self.send_action(content)

    def start_game(self, data):
        self.game_click = 0
        print("game started")
        print(self.game_click,self)
        print("game_click reset")

        content = {
            'command': 'start_game',
        }
        return self.send_action(content)

    def game_clicked(self, data):
        self.game_click += 1
        print(self.game_click,self)
        if self.game_click == self.game_click_goal:
            self.game_get_winner()

    def game_get_winner(self):
        content = {
            'command': 'game_get_winner',
            'winner': self.current_user_json
        }
        return self.send_action(content)

    commands = {
        'new_message': new_message,
        'start_quiz': start_quiz,
        'whoami': whoami,
        'send_reply': send_reply,
        'get_answer': get_answer,
        'next_question': next_question,
        'end_quiz': end_quiz,

        'start_game': start_game,
        'game_click': game_clicked,
        'game_get_winner': game_get_winner
    }

    def user_to_json(self, user):
        return {
            'id': user.id,
            'username': user.username
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_action(self, data):
        # Send action to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'action',
                'data': data
            }
        )

    def action(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))
