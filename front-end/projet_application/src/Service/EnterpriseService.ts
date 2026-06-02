import { enterprises } from "$lib"
import type { Enterprise } from "../Models/Enterprise"
import type { User } from "../Models/User"
import { GET, POST, PUT } from "../ts/server"

export const fetchEnterprises = async () => {
  return await GET<any>("/enterprise/all")
}

export const fetchEnterprisesAsOptions = async () => {
  const response = await GET<any>("/enterprise/all")
  return response.map((e: Enterprise) => {
    return { label: e.name, value: e.id }
  })
}

export const fetchCurrentUserEnterprise = async (): Promise<Enterprise> => {
  const response: Enterprise = await GET<any>("/enterprise/currentEnterprise", false)
  return response
}

export const upsertEnterprise = async (enterprise: Enterprise): Promise<Enterprise> => {
  try {
    const response = enterprise.id && enterprise.id > 0 ?
      await PUT<any, any>(`/enterprise/${enterprise.id}`, enterprise) :
      await POST<any, any>(`/enterprise/new`, enterprise)
    return response.data
  } catch (error) {
    console.error("Error creating enterprise:", error)
    throw error
  }
}