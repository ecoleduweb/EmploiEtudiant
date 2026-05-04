  import type { Enterprise } from "../Models/Enterprise"
  import type { User } from "../Models/User"
  import { GET, POST, PUT } from "../ts/server"

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

  export const checkIfUserHaveEnterprise = async (currentUser: User | undefined) => {
    if (!currentUser?.isModerator)
      return (await getCurrentUserEnterprise() != undefined)
    return false
  }

  export const fetchEnterpriseWithId = async (employerId: number) => {
    return await GET<any>(
      `/enterprise/employer/${employerId}`
    )
  }

  export const updateEnterprise = async (enterprise: Enterprise, enterpriseId: number) => {
    enterprise.userIds = enterprise.users?.map(u => ( u.id )) as any// ne pas envoyer les autres propriétés de l'utilisateur
    delete enterprise.id // le id est poassé dans la rute
    const response = await PUT<any, any>(
        `/enterprise/${enterpriseId}`,
        enterprise,
    )
    return response
  }

  export const createEnterprise = async (enterprise: Enterprise) => {
    enterprise.userIds = enterprise.users?.map(u => ( u.id )) as any// ne pas envoyer les autres propriétés de l'utilisateur
  
    return await POST<Enterprise, Enterprise>(
        `/enterprise/new`,
        enterprise,
    )
  }

  export default fetchAllEnterprises