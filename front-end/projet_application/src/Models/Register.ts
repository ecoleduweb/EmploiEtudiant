import type User from "./User"

export interface Register {
    user: User
    validatePassword: string
    token: string
}
