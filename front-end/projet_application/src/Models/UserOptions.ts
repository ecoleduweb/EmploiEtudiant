import type { User } from "./User";

   export type UserOption = { 
            label: string; 
            value: number; 
            //permet de retrouver les utilisateurs et de les mapper facilement à l'entreprise avant de la mise à jour 
            originalUser: User 
    };