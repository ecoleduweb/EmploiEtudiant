export interface User extends RegisterUser {
    id: number
    isModerator: boolean
    active: boolean
}

export interface RegisterUser {
    email: string
    firstName: string
    lastName: string
    password: string
}

