import axios from 'axios'
import { getJWTToken } from './token'

export function logIn(username, password, rememberMe) {
  return axios.post('/auth/login', {
    username: username,
    password: password
  }, {
    withCredentials: true,
    params: {
      remember: rememberMe ? 'true' : 'false'
    }
  })
    .then(response => {
      return response
    })
}

export function signUp(formData) {
    return axios.post('/auth/register', formData)
    .then(response => {
        return response
      });
}

export function refresh() {
  return axios.post('/api/token/refresh/', {}, {
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
    })
}

export function verifyResetToken(token) {
  return axios.post('/validate/token/reset/', {"ResetToken": token},{
  }).then(response => {
  return response
})
.catch(error=> {
    error = false;
  return error
})
}

export function resetPassword(formData) {
    return axios.post('/token/reset', formData)
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
