import { GET } from "../ts/server";
import type { User } from "../Models/User";

export const fetchAllUsers = async (): Promise<User[]> => {
    try {
        const data = await GET<{ users: User[] }>("/user/all");
        return data?.users || [];
    } catch (error) {
        console.error("Erreur lors de la récupération des utilisateurs:", error);
        throw error;
    }
};