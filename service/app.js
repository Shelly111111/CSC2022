const AppConfig = require('./config')
const express = require('express');
const app = express();
let appConfig = new AppConfig(app)


app.listen(appConfig.listenPort, () => console.log(`Example app listening on port ${appConfig.listenPort}!`))