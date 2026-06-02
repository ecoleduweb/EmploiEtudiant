import type { Enterprise } from "../Models/Enterprise"
import type { User } from "../Models/User"
import { GET } from "../ts/server"

export const fetchEmploymentSchedulesAsOptions = async () => {
  const response = await GET<any>("/employmentSchedule/all")
  return response.map((s: any) => {
    return { label: s.description, value: s.id }
  })
}