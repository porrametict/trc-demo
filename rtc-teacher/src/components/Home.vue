<template>
  <v-app id="keep" v-if="user">
    <v-app-bar
      app
      clipped-left
      color="amber"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer"/>
      <span class="title ml-3 mr-5">RTC-SSS</span>
      <v-spacer/>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
      color="grey lighten-4"
    >
      <v-list flat>
        <v-subheader>{{ user.is_teacher == 1 ? "Teacher" : "Student"}}</v-subheader>
        <v-list-item-group color="amber">
          <v-list-item
          >
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content v-if="user">
              <v-list-item-title>{{user.user}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container
        fluid
        class="fill-height"
      >
        <template v-if="user.is_teacher">
          <RoomTeacher></RoomTeacher>
        </template>
        <template v-else>
          <RoomStudent></RoomStudent>
        </template>
      </v-container>
    </v-content>
  </v-app>
</template>
<script>
    import {mapState} from 'vuex'
    import RoomTeacher from './Room'
    import RoomStudent from './RoomStudent'

    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        },
        components: {
            RoomTeacher, RoomStudent
        },
        computed: mapState({
            user: state => state.user.user
        }),
        created() {
            if (localStorage.token) {
                this.getUser()
            } else {
                this.$router.push({name: "login"})
            }
            console.log(this.user)
        },
        data: () => ({
            data: null,
            drawer: null,
            form: {
                name: "",
                owner: 2,
            },
        }),
        methods: {
            async getUser() {
                this.data = await this.$store.dispatch('user/getCurrentUser', this
                    .form)
            }
        }
    }
</script>
