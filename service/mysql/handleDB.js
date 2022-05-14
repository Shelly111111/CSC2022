const db = require('./nodejs-orm/index')

async function handleDB(res, tableName, methodName, errMsg, n1, n2) {
    let Model = db.model(tableName)
    let result
    try {
        result = await new Promise((resolve, reject) => {
            if (!n1) {
                Model[methodName]((err, data) => {
                    if (err) reject(err)
                    resolve(data)
                })
                return
            }
            if (!n2) {
                Model[methodName](n1, (err, data) => {
                    if (err) reject(err)
                    resolve(data)
                })
                return
            }
            Model[methodName](n1, n2, (err, data) => {
                if (err) reject(err)
                resolve(data)
            })

        })
    } catch (err) {
        console.log(err);
        res.send({ errMsg: errMsg })
        return
    }

    return result
}

module.exports = handleDB