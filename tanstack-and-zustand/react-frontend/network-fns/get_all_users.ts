import axios from 'axios'
import { BackendURI } from '../URI'
export type dbType =  {
    id: string
    name: string
    age: string
}
export default async function getAllUsers() {
    const users: {data: {users: dbType[]}} = await axios.get(`${BackendURI}`)
    return users.data.users||[]
}