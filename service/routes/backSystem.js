const express = require('express');
// 路由模块
const router = express.Router();
// 导入验证码模块
const Captcha = require('../utils/captcha');
// 引入数据库
const handleDB = require('../mysql/handleDB')

// 自定义sql
const db = require('../mysql/nodejs-orm/index')


// 路径
const fs = require('fs')
let path = require('path')
const mineType = require('mime-types');
const multer = require('multer')

//上传文件存放路径
const upload = multer({
    dest: "upload"
});

// 图片转base64 最多五张
router.post("/upload", upload.array('avatar', 5), function(req, res) {
    let filePath = path.join(__dirname, '../', req.files[0].path);
    // console.log(filePath);
    let data = fs.readFileSync(filePath);

    data = Buffer.from(data).toString('base64');

    let base64 = 'data:' + mineType.lookup(filePath) + ';base64,' + data;
    // console.log(base64);

    res.send(base64)

})

// 存储image
router.post('/post_storage_image', (req, res) => {
    (async function() {
        // 获取 post 请求参数 判空
        let {
            imgSrc,
        } = req.body;
        // console.log(req.body);
       

      let result2 = await handleDB(res, "changedetection1", "insert", "数据库插入数据出错", {
            imgSrc,
           
        })
        
        console.log(result2);

        // 返回注册成功给前端
        res.send({
            errno: '0',
            errmsg: "存储成功",
        })

    })()

})

// 存储image
router.post('/post_storage_image2', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空
    let {
      imgSrc,
    } = req.body;
    // console.log(req.body);


    let result2 = await handleDB(res, "changedetection2", "insert", "数据库插入数据出错", {
      imgSrc,

    })

    console.log(result2);

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "存储成功",
    })

  })()

})

// 存储image
router.post('/post_targetextraction_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空
    let {
      imgSrc,
    } = req.body;
    // console.log(req.body);


    let result2 = await handleDB(res, "targetextraction", "insert", "数据库插入数据出错", {
      imgSrc,

    })

    console.log(result2);

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "存储成功",
    })

  })()

})

// 存储image
router.post('/post_terrainclassification_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空
    let {
      imgSrc,
    } = req.body;
    // console.log(req.body);


    let result2 = await handleDB(res, "terrainclassification", "insert", "数据库插入数据出错", {
      imgSrc,

    })

    console.log(result2);

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "存储成功",
    })

  })()

})

// 存储image
router.post('/post_objectdetection_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空
    let {
      imgSrc,
    } = req.body;
    // console.log(req.body);


    let result2 = await handleDB(res, "objectdetection", "insert", "数据库插入数据出错", {
      imgSrc,

    })

    console.log(result2);

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "存储成功",
    })

  })()

})

// 查找image
router.post('/post_find_image1', (req, res) => {
    (async function() {
        // 获取 post 请求参数 判空
       

      let result = await handleDB(res, "changedetection1", "find", "数据库查询出错",)

        // 返回注册成功给前端
        res.send({
            errno: '0',
            errmsg: "查询成功",
            result
        })

    })()

})

// 查找image
router.post('/post_find_image2', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空


    let result = await handleDB(res, "changedetection2", "find", "数据库查询出错",)

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "查询成功",
      result
    })

  })()

})

// 查找image
router.post('/find_targetextraction_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空


    let result = await handleDB(res, "targetextraction", "find", "数据库查询出错",)

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "查询成功",
      result
    })

  })()

})

// 查找image
router.post('/find_terrainclassification_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空


    let result = await handleDB(res, "terrainclassification", "find", "数据库查询出错",)

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "查询成功",
      result
    })

  })()

})

// 查找image
router.post('/find_objectdetection_image', (req, res) => {
  (async function () {
    // 获取 post 请求参数 判空


    let result = await handleDB(res, "objectdetection", "find", "数据库查询出错",)

    // 返回注册成功给前端
    res.send({
      errno: '0',
      errmsg: "查询成功",
      result
    })

  })()

})

module.exports = router
