<template>
  <v-app id="inspire">
    <v-content>
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
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="amber"
                dark
                flat
              >
                <v-toolbar-title>Login</v-toolbar-title>
                <v-spacer />
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    v-model="form.username"
                    label="username"
                    name="username"
                    prepend-icon="mdi-account"
                    type="text"
                  />

                  <v-text-field
                    v-model="form.password"
                    id="password"
                    label="Password"
                    name="password"
                    prepend-icon="mdi-key"
                    type="password"
                  />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn color="amber" @click="login">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        },
        created () {
            // console.log("cat")
        },
        data : () => ({
            form : {
                username: "",
                password : ""
            },
            token : null
        }),
        methods : {
            async login () {
                localStorage.setItem('token',"")
                this.token = await this.$store.dispatch('user/getUserToken',this
                    .form)
                if(this.token != null ){
                     this.$router.push({name:'Home'})
                }

        }
        }
    }
</script>
