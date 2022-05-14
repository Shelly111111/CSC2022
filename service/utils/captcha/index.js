// yarn add svg-captcha
var svgCaptcha = require('svg-captcha');


class Captcha{


    getCode(){
        var captcha = svgCaptcha.create({ 
            inverse: false, // 翻转颜色 
            fontSize: 48, // 字体大小 
            noise: 2, // 噪声线条数 
            width: 100, // 宽度 
            height: 40, // 高度 
            size: 4,// 验证码长度
            ignoreChars: '0o1i', // 验证码字符中排除 0o1i
        }); 
        return captcha
    }
    
}
 

// let captchaObj = new Captcha();
// let captcha = captchaObj.getCode();
// console.log(captcha.text)
// console.log(captcha.text.toLowerCase());
// console.log(String(captcha.data));    //将来要发送给客户端的数据


module.exports = Captcha