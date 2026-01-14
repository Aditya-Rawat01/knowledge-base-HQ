import {  useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import './App.css'
import getAllUsers from '../network-fns/get_all_users'
import {updateUser} from "../network-fns/update_user"
import {addUser} from "../network-fns/add_user"
import {deleteUser} from "../network-fns/delete_user"
import {useCounterStore} from "../zustand-store/store"

function App() {
  const {counter, increaseCounter, decreaseCounter} = useCounterStore()
  const queryClient = useQueryClient()
  const {isPending:dataPending, data:users} = useQuery({queryKey: ['users'], queryFn: getAllUsers})
  const udpateUserMutation = useMutation({
    mutationFn: (id:string) => updateUser(id),
    onSuccess: async() =>{
      await queryClient.invalidateQueries({queryKey: ['users']})  // invalidating getAllUsers
    }
  })
  const addUserMutation = useMutation({
    mutationFn: () => addUser(),
    onSuccess: async() =>{
      await queryClient.invalidateQueries({queryKey: ['users']})  // invalidating getAllUsers
    }
  })
  const deleteUserMutation = useMutation({
    mutationFn: (id:string) => deleteUser(id),
    onSuccess: async() =>{
      await queryClient.invalidateQueries({queryKey: ['users']})  // invalidating getAllUsers
    }
  })


  if (udpateUserMutation.isPending || addUserMutation.isPending || deleteUserMutation.isPending) {
    return <div className='screen'>
      updating users!!!
    </div>
  }
  if (dataPending) {
    return <div className='screen'>
      getting all the users!
    </div>
  }
  return (
    <div className='screen'>
        <p>Total Users:  {counter}</p>
      <div className='modal'>
        {users!.map((user)=>{
          return <div className='user'>
            <p>Name: {user.name}</p>
            <p>Age: {user.age}</p>
            <button onClick={(_e, id=user.id)=>udpateUserMutation.mutate(id)}>update</button>
            <button onClick={(_e, id=user.id)=>{
              deleteUserMutation.mutate(id)
              decreaseCounter()
              }}>delete</button>
          </div>
        })}
          <button onClick={(_e)=>{
            addUserMutation.mutate()
            increaseCounter()
            }}>Add new User</button>
      </div>
    </div>
  )
}

export default App
