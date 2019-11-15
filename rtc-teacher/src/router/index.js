import Vue from 'vue'
import Router from 'vue-router'

function view(name) {
    return function (resolve) {
        require(['@/components/' + name + '.vue'], resolve);
    }
}

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: view("Login")
    },{
      path: '/home',
      name: 'Home',
      component: view("Home")
    },
  ]
})
