<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        cols="12"
        align="center"
      >
        <template v-if="quiz_state === 'off' ">
          <h1>สถานะปกติ</h1>
        </template>

        <template v-if="quiz_state === 'Qshow'" align-self="start" class="fill-height">
          <div class="d-flex justify-center align-center fill-height">
            <v-card
              class="mx-auto"
              outlined
              align="start"
              width="100%"

            >
              <v-card-text>
                <div class="overline mb-4">คำถาม</div>
                <v-divider></v-divider>
                <h1 class="display-3 text-center">{{question_set[current_question].question}}</h1>
                <v-divider class="my-5"></v-divider>
                <template v-for="(ans,index) in question_set[current_question].answer_set" v-if="show_choice === true">
                  <v-btn :key="index" block x-large outlined color="deep-orange accent-4" @click="send_reply(current_question,ans)" class="my-2">
                    {{ans.answer}}
                  </v-btn>
                </template>
              </v-card-text>
            </v-card>
          </div>
        </template>

        <template v-if="quiz_state === 'wait_answer'">
          <h1>คุณส่งคำตอบเเล้ว</h1>
        </template>
        <template v-if="quiz_state=== 'get_answer'">
          <template>
            <template v-if="selected_choice_set[current_question].selected_choice.is_correct === true ">
              <v-icon size="200" color="green">mdi-emoticon-happy</v-icon>
              <h1>Correct</h1>
            </template>
            <template v-else>
              <v-icon size="200" color="red">mdi-emoticon-angry</v-icon>
              <h1>InCorrect</h1>
            </template>
          </template>
        </template>
        <template v-if="quiz_state === 'end_quiz'" class="fill-height">

          <div class="d-flex justify-center align-center fill-height">
            <v-card
              class="mx-auto"
              max-width="500"
              outlined
              align="start"
            >
              <v-card-text>
                <div class="overline mb-4">summary</div>
                <h1>คุณได้ {{get_score()}} คะเเนน</h1>
              </v-card-text>

              <v-card-actions>
                <v-btn @click="quiz_end" color="amber" block>End</v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </template>


        <template v-if="quiz_state === 'start_game'">
          <h3 class="display-1 my-5">คลิกให้เร็วที่สุดเพื่อชนะ</h3>
          <v-icon color="amber" size="300" @click="sent_click_to_game">mdi-star-circle</v-icon>
        </template>
        <template v-if="quiz_state === 'game_get_winner'">
          <template>
            <v-icon color="amber" size="300" >mdi-emoticon-neutral-outline</v-icon>
            <h1>เสียใจด้วย คุณไม่มีโอกาศตอบ</h1>
          </template>
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
            quiz_state: 'off',
            quiz_mode: null,
            show_choice: true,
            current_question: 0,
            question_set: [],
            selected_choice_set: [],
            game_clicked : 0

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
                    } else if (data['command'] === 'start_quiz') {
                        vm.quiz_mode = data['mode']
                        vm.on_start_quiz(data['questions'])
                    } else if (data['command'] === 'get_answer') {
                        if(vm.quiz_state !== 'game_get_winner') {
                            vm.quiz_state = 'get_answer'
                        }

                    } else if (data['command'] === 'next_question') {
                        vm.quiz_state = 'Qshow'
                        vm.current_question = data['next_question']

                        if (vm.quiz_mode === 'single') {
                            vm.show_choice = false
                        }
                    } else if (data['command'] === 'end_quiz') {
                        vm.quiz_state = 'end_quiz'
                    } else if (data['command'] === 'start_game') {
                        vm.on_game_started()
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
            on_start_quiz(questions) {
                this.quiz_state = 'Qshow'
                this.question_set = questions

                if (this.quiz_mode === 'single') {
                    this.show_choice = false
                }
            },
            send_reply(question, choice) {
                this.selected_choice_set.push(
                    {
                        question_no: question,
                        selected_choice: choice
                    }
                )
                this.chat_socket.send(JSON.stringify({
                    'command': 'send_reply',
                    'data': this.selected_choice_set[this.current_question]
                }));
                this.quiz_state = 'wait_answer'
            },
            get_score() {
                let c = _.filter(this.selected_choice_set, function (o) {
                    return o.selected_choice.is_correct === true;
                });
                return c.length
            },
            quiz_end() {
                this.question_set = []
                this.selected_choice_set = []
                this.current_question = 0
                this.quiz_state = 'off'
                this.quiz_mode = null
                this.show_choice = true
            },


            on_game_started() {
                this.quiz_state = 'start_game'
                this.game_clicked = 0
                this

            },
            sent_click_to_game() {
                // this.game_clicked += 1
                // let goal = 10
                // if(this.game_clicked === goal) {
                //
                //     this.chat_socket.send(JSON.stringify({
                //         'command': 'game_get_winner',
                //     }));
                //
                // }

                this.chat_socket.send(JSON.stringify({
                    'command': 'game_click',
                }));

            },
            on_game_get_winner(data) {
                let game_winner = data['winner'].username
                console.log(game_winner, this.user)
                if (game_winner === this.user.user) {
                    this.quiz_state = 'Qshow'
                    let vm = this
                    setTimeout(function () {
                        vm.show_choice = true
                        console.log("show")
                    },1000)
                } else {
                    this.send_reply(
                        this.current_question,
                        {
                            answer: "no answer",
                            is_correct: false
                        },
                    )
                    this.quiz_state = 'game_get_winner'
                }
            }
        }
    }
</script>

<style scoped>

</style>
