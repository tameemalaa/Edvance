// Function to set the JWT token in an HTTP-only cookie
export function setJWTToken(token) {
    // Set the "jwt" cookie with the JWT token and the "HttpOnly" flag
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
  
    return null;
  }
  