function fn() {
  var config = { baseUrl: karate.properties['baseUrl'] || 'http://127.0.0.1:3000' };
  var auth = karate.callSingle('classpath:auth-token.feature', config);
  config.authToken = auth.token;
  return config;
}
