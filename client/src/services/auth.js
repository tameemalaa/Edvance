import axios from 'axios'
import { getJWTToken } from './token'

export function logIn(username, password, rememberMe) {
  return axios.post('/auth/jwt/create/', {
    username: username,
    password: password
  }, {
    // withCredentials: true,
    params: {
      remember: rememberMe ? 'true' : 'false'
    }
  })
    .then(response => {
      return response
    })
}

export function signUp(formData) {
    return axios.post('/auth/users/', formData)
    .then(response => {
        return response
      });
}

export function refresh() {
  return axios.post('/auth/jwt/refresh/', {}, {
    withCredentials: true
  })
    .then(response => {
      return response
    })
}

export function signOut() {
  return axios.post('/api/token/logout/', {}, {
    withCredentials: true
  })
    .finally(() => {
        this.$cookies.remove('myCookie');
    })
}

export function verifyResetToken(token) {
  return axios.post('auth/users/reset_password_confirm', {"ResetToken": token},{
  }).then(response => {
  return response
})
.catch(error=> {
    error = false;
  return error
})
}
export function verifyActivationToken(token,uid) {
  console.log(token)
  return axios.post('auth/users/activation/', {"token": token,"uid": uid},{
  }).then(response => {
  return response
})
.catch(error=> {
  console.log(error)
    error = false;
  return false
})

}

export function resetPassword(formData) {
    return axios.post('auth/users/reset_password/', formData)
    .then(response => {
        return response
      });

}

export function authHeader() {
  return {
    'Authorization': `Bearer ${getJWTToken()}`
  }
}

axios.interceptors.request.use(
  (config) => {
    config.headers.Authorization = `Bearer ${getJWTToken()}`
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
