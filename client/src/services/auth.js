// Import axios and getJWTToken function
import axios from 'axios'
import { getJWTToken } from './token'


// Function to authenticate a user and set the JWT token in an HTTP-only cookie
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

// Function to refresh the JWT token using an HTTP-only cookie
export function refresh() {
  return axios.post('/api/token/refresh/', {}, {
    withCredentials: true
  })
    .then(response => {
      return response
    })
}

// Function to sign out a user and remove the JWT token from the HTTP-only cookie
export function signOut() {
  return axios.post('/api/token/logout/', {}, {
    withCredentials: true
  })
    .finally(() => {
      // Do any additional clean-up, if necessary
    })
}

// Function to check if the user is authenticated
export function isAuthenticated() {
  return axios.get('/api/token/verify/', {
    withCredentials: true
  })
    .then(response => {
        response= true;
      return response
    })
    .catch(error=> {
        error = false;
      return error
    })
}

// Function to get the CSRF token from Django's cookies
function getCSRFToken() {
  const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)
  if (csrfToken !== null) {
    return csrfToken[1]
  }
  return null
}

// Function to include the CSRF token and the JWT token in the headers of an axios request
export function authHeader() {
  return {
    'X-CSRFToken': getCSRFToken(),
    'Authorization': `Bearer ${getJWTToken()}`
  }
}


// Add a request interceptor to include the JWT token in the headers of all requests
axios.interceptors.request.use(
  (config) => {
    config.headers.Authorization = `Bearer ${getJWTToken()}`
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
