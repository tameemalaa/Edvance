import VueCookies from 'vue-cookies';

export function setJWTToken(token) {
  console.log(token)
  if (!token) {
    VueCookies.remove('jwt');
    console.log('removed jwt')
    return;
  }
  VueCookies.set('jwt', token, '1d', null, 'Strict');
}

export function getJWTToken() {
  return VueCookies.get();
}