const cookieParser = require('cookie-parser');
const cookieSession = require('cookie-session');

// 1、引入body-parser
const bodyParser = require('body-parser');
// 引入路由
const backSystem = require('./routes/backSystem');
// 跨域
const cors = require('cors');


class AppConfig {
    constructor(app) {
        this.app = app;
        this.listenPort = 3001;
        // 跨域
        app.use(cors());
        // 获取post请求参数的配置
        this.app.use(bodyParser.urlencoded({
            limit: '50mb',
            extended: true
        }));
        this.app.use(bodyParser.json({
            limit: '50mb',
        }));

        // 注册cookie 和sesison
        this.app.use(cookieParser());
        this.app.use(cookieSession({
            name: "my_session",
            keys: ["%$#^&^%&TSFR#$TRGDRG$%GFDG%^$#%#^GFDGRDHG$#@^Y%"],
            maxAge: 1000 * 60 * 60 * 24 * 2 // 2天
        }))


        // 注册路由
        this.app.use(backSystem)

    }

}

module.exports = AppConfig