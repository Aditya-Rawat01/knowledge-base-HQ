import axios from 'axios'
import { BackendURI } from '../URI'

export async function updateUser(id:string) {
    const names = ["Adam", "Eve", "John", "Jane"]
    const newName = names[Math.floor(Math.random()*4)]
    const newAge = Math.floor(Math.random()*20 + 20)
    await axios.post(`${BackendURI}/update-user`, {
        "id": id,
        "name": newName,
        "age": newAge
    })
}