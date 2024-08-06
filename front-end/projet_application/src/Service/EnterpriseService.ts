import type { Enterprise } from "../Models/Enterprise"
import { GET } from "../ts/server"

const fetchAllEnterprises = async () => {
  const response = await GET<any>("/enterprise/all")
  return response.map((e: Enterprise) => {
    return { label: e.name, value: e.id }
  })
}

export const getCurrentUserEnterprise = async () => {
  const response: Enterprise = await GET<any>("/enterprise/currentEnterprise")
  return response
}

export const fetchEnterpriseWithId = async (employerId: number) => {
  return await GET<any>(
    `/enterprise/employer/${employerId}`
  )
}

export default fetchAllEnterprises