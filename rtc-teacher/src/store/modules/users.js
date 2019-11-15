export default {
    namespaced : true,
    state : {
      user : null,

    },
    mutations : {
      setUser(state,data) {
        state.user = data
      }
    },
    actions : {
        async getUserToken (context,params = null ) {
            let result  = await axios.post("/api/account/login",params)
                .then( (response) => {
                    localStorage.setItem('token',response.data.token)
                  console.log(response.data)
                  return response.data.token
                })
                .catch((error) => {
                     console.log(error.message)
                    return error.message
                })
            return result
        },
      async getCurrentUser (context,params = null ) {
        let result  = await axios.get("/api/account/current_user",params)
          .then( (response) => {

            context.commit("setUser",response.data)
            return response.data.token
          })
          .catch((error) => {
            console.log(error.message)
            return error.message
          })
        return result
      },
      async postTeacherRegistration (context,params = null ) {
            let result  = await axios.post("/api/account/teacher_register",params)
                .then( (response) => {
                  return response.data
                })
                .catch((error) => {
                     console.log(error.message)
                    return error.message
                })
            return result
        },
      async postStudentRegistration (context,params = null ) {
        let result  = await axios.post("/api/account/student_register",params)
          .then( (response) => {
            return response.data
          })
          .catch((error) => {
            console.log(error.message)
            return error.message
          })
        return result
      },
    }
}
