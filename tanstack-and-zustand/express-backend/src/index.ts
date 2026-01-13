import express, { type NextFunction } from 'express'
import { type Request, type Response } from 'express'
import cors from 'cors'
import { randomUUID } from 'node:crypto'

const app = express()
app.use(express.json())
app.use(cors())
type dbType =  {
    id: string
    name: string
    age: string
}
// to *simulate* a persistent database.
let db: dbType[] = []

function BodyMiddleware(req:Request, res: Response, next: NextFunction) {
    if (!req.body) {
        return res.status(400).json({
            "msg": "No body provided!"
        })
    }
    next()
}

app.get("/",(req:Request, res: Response)=>{
    return res.json({
        "msg": "all user fetched successfully",
        "users": db
    })
})

app.post("/add-user", BodyMiddleware, (req:Request, res: Response)=>{
    
    const {name, age} = req.body

    if (!name || !age) {
        return res.json({
            "msg": "Incomplete fields"
        })
    }
    const id = randomUUID()
    const user = {id, name, age}
    db.push(user)
    return res.json({
        "msg": "updated users in db"
    })
})


app.post("/update-user", BodyMiddleware, (req:Request, res: Response)=>{
    
    const {id, name, age} = req.body

    if (!id || !name || !age) {
        return res.json({
            "msg": "Incomplete fields"
        })
    }
    const uniqueUser = db.find((user)=>user.id == id)
    if (!uniqueUser) {
        return res.json({
            "msg": "No such user found"
        })
    }
    uniqueUser.name = name
    uniqueUser.age = age

    return res.json({
        "msg": "User updated successfully!"
    })

})

app.post("/delete-user", BodyMiddleware, (req:Request, res: Response)=>{
    
    const {id} = req.body

    if (!id) {
        return res.json({
            "msg": "Incomplete fields"
        })
    }
    db = db.filter((user)=>user.id != id) // filtering and then reassigning then copy to same array variable.

    
    return res.json({
        "msg": "User deleted successfully!",
    })

})


app.listen(3000, ()=>{
    console.log("Server started at port: 3000")
})