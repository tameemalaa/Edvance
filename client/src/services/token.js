import VueCookies from 'vue-cookies';

export function setJWTToken(token) {
  VueCookies.set('jwt', token, '1d', null, 'Strict');
}

export function getJWTToken() {
  return VueCookies.get();
}