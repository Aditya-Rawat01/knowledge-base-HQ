import axios from 'axios'
import { BackendURI } from '../URI'

export async function addUser() {
    const names = ["Adam", "Eve", "John", "Jane"]
    const name = names[Math.floor(Math.random()*4)]
    const age = Math.floor(Math.random()*20 + 20)
    await axios.post(`${BackendURI}/add-user`, {
        "name": name,
        "age": age
    })
}