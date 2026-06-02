import type { User } from "../Models/User"
import type { Option } from "../Models/Option"
import { GET } from "../ts/server"

export const fetchUsers = async () => {
  return await GET<User[]>("/user/all")
}

export const fetchUsersAsOptions = async (): Promise<Option[]> => {
  const users = await fetchUsers()
  return users.map((u: User) => {
    return { label: `${u.firstName} ${u.lastName} (${u.email})`, value: u.id }
  })
}