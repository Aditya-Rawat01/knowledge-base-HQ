import axios from 'axios'
import { BackendURI } from '../URI'

export async function deleteUser(id:string) {
    await axios.post(`${BackendURI}/delete-user`, {
        "id" : id
    })
}