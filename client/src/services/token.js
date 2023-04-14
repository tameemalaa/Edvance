export function setJWTToken(token) {
    document.cookie = `jwt=${token}; HttpOnly; Secure; SameSite=Strict`
  }
export function getJWTToken() {
    const name = 'jwt=';
    const cookies = document.cookie.split(';');
  
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.startsWith(name)) {
        return cookie.substring(name.length, cookie.length);
      }
    }
  
  }
  