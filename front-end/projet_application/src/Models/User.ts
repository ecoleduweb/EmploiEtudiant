export interface User {
    id: number
    email: string
    firstName: string
    lastName: string
    isModerator: boolean
    active: boolean
}

export interface RegisterUser {
    email: string
    firstName: string
    lastName: string
    password: string
}

