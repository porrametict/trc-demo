<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
      class="fill-height"
      align="center"
      justify="center"
    >
      <v-col
        class="fill-height"
        cols="12"
        align="center"
      >
        <template v-if="quiz_state === 'off' ">
          <v-card class="mx-auto " outlined>
            <v-toolbar
              color="grey"
              dark
              flat
            >
              <v-toolbar-title>Question</v-toolbar-title>
              <v-spacer/>
              Mode :
              <v-radio-group v-model="quiz_mode" :mandatory="false">
                <v-row class="mt-6 ml-1">
                  <v-col cols="6">
                    <v-radio label="Single" value="single"></v-radio>
                  </v-col>
                  <v-col cols="6">
                    <v-radio label="Multiple" value="multiple"></v-radio>
                  </v-col>
                </v-row>
              </v-radio-group>
              <v-spacer></v-spacer>
              <v-btn color="white" light @click="add_question">Add Question</v-btn>
            </v-toolbar>
            <template>
              <v-card-text v-for="(q,index) in question_set" :key="index">
                <v-row class="mx-5">
                  <v-text-field v-model="q.question"
                                label="คำถาม"
                                prepend-icon="mdi-help-rhombus"
                                append-icon="mdi-close"
                                @click:append="delete_question(index)"
                  ></v-text-field>
                </v-row>

                <v-row class="mx-5">
                  <template v-for="(a,index) in q.answer_set">
                    <v-col cols="12">
                      <v-row align="center">
                        <v-checkbox
                          v-model="a.is_correct"
                          hide-details
                          class="shrink mr-2 mt-0"
                        ></v-checkbox>
                        <v-text-field label="ตัวเลือก" v-model="a.answer"></v-text-field>
                      </v-row>
                    </v-col>
                  </template>
                </v-row>
              </v-card-text>
              <v-btn color="amber" large @click="start_quiz" class="mb-3">Start Quiz</v-btn>
            </template>

          </v-card>

        </template>

        <template v-if="quiz_state === 'Qshow'" class="fill-height">
          <div class="d-flex justify-end mb-12">
            <v-card>
              <v-card-text v-if="quiz_mode==='multiple'">
                <span v-if="quiz_mode === 'multiple'" class="mx-5">จำนวนคนตอบ :
                 <span>{{getCountReply('all')}}</span>
                </span>
                <v-btn @click="get_answer" v-if="show_ans_btn" color="primary">เฉลย</v-btn>
              </v-card-text>

              <v-card-text v-if="quiz_mode==='single'">
                <span class="mx-5" v-if="show_ans_btn===false">รอผู้ชนะ</span>
                <v-btn @click="get_answer" v-if="show_ans_btn" color="primary">เฉลย</v-btn>
              </v-card-text>
            </v-card>
          </div>

          <div class="d-flex justify-center align-center mt-12">
            <v-col>
            <h1 class="display-3">{{question_set[current_question].question}}</h1>
            <template v-if="quiz_mode === 'single' && show_ans_btn">
              <v-divider class="my-5"></v-divider>
              <span class="headline">{{game_winner.user.username}} ตอบ {{game_winner.ans.selected_choice.answer}}</span>
            </template>
          </v-col>
          </div>
        </template>

        <template v-if="quiz_state === 'get_answer'" class="fill-height">

          <div class="d-flex justify-center align-center fill-height">
            <v-card
              class="mx-auto"
              max-width="500"
              min-width="500"
              outlined
              align="start"
            >
              <v-list-item v-if="quiz_mode==='multiple'">
                <v-list-item-content >
                  <div class="overline mb-4">result</div>
                  <v-list-item-title class="headline mb-1">จำนวนคนตอบ : {{getCountReply('all')}}</v-list-item-title>
                  <v-list-item-title class="headline mb-1">ตอบถูก : {{getCountReply(true)}}</v-list-item-title>
                  <v-list-item-title class="headline mb-1">ตอบผิด : {{getCountReply(false)}}</v-list-item-title>
                </v-list-item-content>

              </v-list-item>

                <v-card-text v-else align="center">
                <div class="overline mb-4 text-start">result</div>
                <template v-if ="game_winner.ans.selected_choice.is_correct === true">
                  <p class="headline mb-1">
                    Correct
                  </p>
                  <v-icon size="100" color="green">mdi-emoticon-happy</v-icon>
                </template>
                <template v-else>
                  <p class="headline mb-1">
                    Incorrect
                  </p>
                  <v-icon size="100" color="red">mdi-emoticon-angry</v-icon>
                </template>
              </v-card-text>

              <v-card-actions>
                <v-btn @click="next_q" block v-if="current_question +1 < question_set.length"  color="primary">Next</v-btn>
                <template v-else>
                  <v-btn @click="get_summary" block color="primary">Report</v-btn>
                </template>
              </v-card-actions>
            </v-card>
          </div>

        </template>

        <template v-if="quiz_state === 'show_report'" class="fill-height">

          <div class="d-flex justify-center align-center fill-height">
            <v-card
              class="mx-auto"
              max-width="500"
              outlined
              align="start"
            >
              <v-card-text>
                <div class="overline mb-4">summary</div>
                <template  v-for="s in get_summary()">
                <h1>
                  {{s.user.username}} : {{s.score}} points
                </h1>
                <v-divider class="my-3"></v-divider>
                </template>
              </v-card-text>
              <v-card-actions>
                <v-btn @click="end_quiz" block color="amber">End</v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </template>
      </v-col>
    </v-row>
  </v-container>

</template>
<script>
    import {mapState} from 'vuex'

    export default {
        name: "Room",
        data: () => ({
            roomName: 'test_room',
            chat_socket: null,
            message: "",
            messages_data: [],
            quiz_mode: 'multiple',
            quiz_state: 'off',
            show_ans_btn: true,
            game_winner: {
                user: null,
                ans: null
            },
            current_question: 0,
            reply_user: [],
            question_set: [
                {
                    question: "1 + 1 = ?",
                    answer_set:
                        [
                            {
                                answer: "2",
                                is_correct: true
                            },
                            {
                                answer: "3",
                                is_correct: false
                            },
                        ]
                },
                {
                    question: "การประกาศตัวแปรใน python ข้อใดถูกต้อง",
                    answer_set:
                        [
                            {
                                answer: "pi = 3.14",
                                is_correct: true
                            },
                            {
                                answer: "let pi = 3.14; ",
                                is_correct: false
                            },
                        ]
                }, {
                    question: "หากนิสิตต้องการขอลาออกจากการศึกษา ควรยื่นคำร้องใด",
                    answer_set:
                        [
                            {
                                answer: "UP08",
                                is_correct: false
                            },
                            {
                                answer: "UP14",
                                is_correct: true
                            },
                        ]
                }
            ]
        }),
        created() {
            this.new_websocket()
        },
        computed: mapState({
            user: state => state.user.user
        }),
        methods: {
            new_websocket() {
                let vm = this
                this.chat_socket = new WebSocket(
                    `ws://127.0.0.1:8000/ws/chat/${this.roomName}/`
                )
                //connect
                this.chat_socket.onopen = function () {
                    console.log('connect chat_socket')
                    vm.whoami()
                }

                //onmessage
                this.chat_socket.onmessage = function (e) {
                    let data = JSON.parse(e.data);

                    if (data['command'] === 'new_message') {
                        vm.messages_data.push(data)
                    } else if (data['command'] === 'send_reply') {
                        vm.on_send_reply(data)
                    } else if (data['command'] === 'game_get_winner') {
                        vm.on_game_get_winner(data)
                    }
                };

                this.chat_socket.onclose = function (e) {
                    console.error('Chat socket closed unexpectedly');
                }
            },
            whoami() {
                if (this.user) {
                    this.chat_socket.send(JSON.stringify({
                        'command': 'whoami',
                        'user': this.user.user
                    }));
                }
            },
            send_message() {
                this.chat_socket.send(JSON.stringify({
                    'command': 'new_message',
                    'message': this.message,
                }));
            },
            start_quiz() {
                this.chat_socket.send(JSON.stringify({
                    'command': 'start_quiz',
                    'questions': this.question_set,
                    'mode': this.quiz_mode,
                }));
                this.quiz_state = 'Qshow'

                if (this.quiz_mode === 'single') {
                    this.show_ans_btn = false
                    setTimeout(this.start_game, 3000)
                }
            },
            start_game() {
                this.show_ans_btn = false
                this.game_winner = {}
                this.chat_socket.send(JSON.stringify({
                    'command': 'start_game',
                }))
            },
            on_send_reply(data) {
                this.reply_user.push(data['data'])
                if (this.quiz_mode === 'single') {
                    this.check_is_winner(data)
                }

            },
            get_answer() {
                this.quiz_state = 'get_answer'
                this.chat_socket.send(JSON.stringify({
                    'command': 'get_answer',
                }));

            },
            getCountReply(data) {
                let current_question = this.current_question
                let c;
                if (data === 'all') {
                    c = _.filter(this.reply_user, function (o) {
                        return o.data.question_no === current_question;
                    });
                } else {
                    c = _.filter(this.reply_user, function (o) {
                        return o.data.selected_choice.is_correct === data && o.data.question_no === current_question;
                    });
                }
                return c.length
            },
            next_q() {
                this.current_question += 1
                this.quiz_state = 'Qshow'
                this.chat_socket.send(JSON.stringify({
                    'command': 'next_question',
                    'next_question': this.current_question
                }));
                if (this.quiz_mode === 'single') {
                    this.show_ans_btn = false
                    this.game_winner = {}
                    setTimeout(this.start_game, 3000)
                }
            },
            end_q() {
                this.chat_socket.send(JSON.stringify({
                    'command': 'end_quiz',
                }));
            },
            end_quiz() {
                this.question_set = []
                this.reply_user = []
                this.current_question = 0
                this.quiz_state = 'off'
                this.add_question()

            },
            get_summary() {
                let users = []
                let scores = []
                let vm = this
                this.reply_user.forEach((e) => {
                    if (!vm.user_exit(users, e.user)) {
                        users.push(e.user)
                    }
                })
                console.log(users)
                users.forEach((e) => {
                    let s = this.get_user_score(e.id)
                    scores.push({user: e, score: s})
                })
                this.end_q()
                this.quiz_state = 'show_report'
                return scores
            },
            user_exit(users, user) {
                let is_exit = false
                users.forEach(e => {
                    if (e.id === user.id) {
                        is_exit = true
                        return 0;
                    }
                })
                return is_exit
            },
            get_user_score(user_id) {
                let c = _.filter(this.reply_user, function (o) {
                    return o.data.selected_choice.is_correct === true && o.user.id === user_id;
                });
                return c.length
            },
            on_game_get_winner(data) {
                this.game_winner.user = data['winner']
            },
            check_is_winner(data) {
                if (data.data.user.username === this.game_winner.user.username) {
                    this.show_ans_btn = true
                    this.game_winner['ans'] = data.data.data
                }
            },
            delete_question(index) {
                this.question_set.splice(index, 1)
            },
            add_question() {
                this.question_set.push(
                    {
                        question: "",
                        answer_set:
                            [
                                {
                                    answer: "",
                                    is_correct: false
                                },
                                {
                                    answer: "",
                                    is_correct: false
                                },
                            ]
                    }
                )
            },


        }
    }
</script>

<style scoped>

</style>
