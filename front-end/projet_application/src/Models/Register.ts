import type { RegisterUser } from "./User"

export interface Register {
    user: RegisterUser;
    validatePassword: string;
    token: string;
}
