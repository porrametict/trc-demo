import Vue from 'vue'
import Vuex from 'vuex'

import user from './modules/users'
import subject from "./modules/subject";

// function store(name) {
//     return function (resolve) {
//         require(['./modules/' + name], resolve);
//     }
// }

Vue.use(Vuex);

export  default  new Vuex.Store({
    namespaced: true,
    modules : {
        user : user,
        subject : subject
    }
})
