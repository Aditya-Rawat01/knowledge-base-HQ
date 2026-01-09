import  express, { type NextFunction, type Request, type Response } from 'express'
import cookieParser from 'cookie-parser'
const app = express()
app.use(express.json())
app.use(cookieParser('the-string-to-sign-cookies'))


// traditional way of handling sessions:

// authenticated route: /authenticated 
// open route: /
// when refresh token expires then just redirect to login. (conceptually.)

function accessToken(req:Request, res:Response, next:NextFunction) {
    const cookies = req.signedCookies
    if (!cookies['access-token']) { 
        if (!cookies['refresh-token']) {
        return res.status(401).json({
            "msg" : "not authenticated, dude!"
        })
    } else {
        renewaccessToken(res)
        next()
    }
    } else {
        next()
    }
}
function renewaccessToken(res:Response) {
    console.log('access-token got renewed without the user knowing!')
    res.cookie('access-token', 'abcdefgh', {maxAge:1000 * 60 * 1, httpOnly: true, secure: true, sameSite: true, signed: true})
    return
}
app.get('/', (req: Request,res: Response)=>{

    res.cookie('access-token', 'abcdefgh', {maxAge:1000 * 60 * 1, httpOnly: true, secure: true, sameSite: true, signed: true}) // secure: true sends cookies on https only.
    res.cookie('refresh-token', 'abcdefgh', {maxAge:1000 * 60 * 15, httpOnly: true, secure: true, sameSite: true, signed: true}) // sameSite: true prevents any csrf attacks

    return res.json({
        "msg": "hello random user"
    })
})


app.get('/authenticated', accessToken, (req,res)=>{
    return res.json({
        "msg": "hello authenticated user"
    })
})

app.listen(3000, ()=>{console.log("traditional token server started!")})