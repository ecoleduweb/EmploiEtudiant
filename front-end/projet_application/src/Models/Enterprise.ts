import type { User } from "./User"

export type Enterprise = {
    id?: number
    name: string
    email: string
    phone: string
    address: string
    cityId: number
    isTemporary: boolean
    users?:User[] 
    userIds?:number[] 
}
