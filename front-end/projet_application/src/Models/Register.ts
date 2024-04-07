import type User from './User';

export interface Register { 
    user: User;
    address: string;
    city: string;
    phone: string;
    nameEnterprise: string;
    zipCode: string;    
    province: string;
    validatePassword: string;
}