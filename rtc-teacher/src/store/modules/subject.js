export default {
    namespaced : true,
    state : {},
    mutations : {},
    actions : {
        async postSubject (context,params = null ) {
            let result  = await axios.post("/account/teacher/subject/",params)
                .then( (response) => {
                  return response.data
                })
                .catch((error) => {
                     console.log(error.message)
                    return error.message
                })
            return result
        },
      async getSubject (context,params = null ) {
            let result  = await axios.get("/account/subject_all/",params)
                .then( (response) => {
                  return response.data
                })
                .catch((error) => {
                     console.log(error.message)
                    return error.message
                })
            return result
        }
    }
}
