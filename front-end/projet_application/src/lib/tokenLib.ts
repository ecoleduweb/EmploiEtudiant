import { jwtDecode } from "jwt-decode";
import type Token from "../Models/Token";
import { currentUser, isLoggedIn, session } from "$lib";
import { goto } from "$app/navigation";



export const logIn = (isModerator: boolean, email: string, firstName: string, lastName: string) => {
  currentUser.set({ isModerator, email, firstName, lastName } as any)
  isLoggedIn.set(true)
  goto("/dashboard")

}

export const setInfoFromDecoded = (decoded: any) => {
  currentUser.set(decoded)
  isLoggedIn.set(true)
}