import type { Enterprise } from "../Models/Enterprise"
import type { User } from "../Models/User"
import { GET } from "../ts/server"

const fetchAllEnterprises = async () => {
  const response = await GET<any>("/enterprise/all")
  return response.map((e: Enterprise) => {
    return { label: e.name, value: e.id }
  })
}

export const getCurrentUserEnterprise = async () => {
  const response: Enterprise = await GET<any>("/enterprise/currentEnterprise", false)
  return response
}

export const userHaveEnterprise = async (currentUser: User | undefined) => {
  try {
    if (!currentUser?.isModerator)
      if (await getCurrentUserEnterprise() != undefined)
        return true
    return false
  }
  catch (err) {
    return false //Indiquer que l'utilisateur n'a pas d'entreprise en cas d'erreur sur la recherche
  }
}

export const fetchEnterpriseWithId = async (employerId: number) => {
  return await GET<any>(
    `/enterprise/employer/${employerId}`
  )
}

export default fetchAllEnterprises