import { currentUser, isLoggedIn } from "$lib";
import { goto } from "$app/navigation";
import type { User } from "../Models/User";



export const logIn = async (user: User) => {
  currentUser.set(user)
  isLoggedIn.set(true)
  await goto("/dashboard")

}

export const setInfoFromDecoded = (decoded: any) => {
  currentUser.set(decoded)
  isLoggedIn.set(true)
}