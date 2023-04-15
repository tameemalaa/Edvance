export function setJWTToken(token) {
  this.$cookies.set('jwt', token, '1d', null, 'Strict');
}

export function getJWTToken() {
  return this.$cookies.get('jwt');
}
