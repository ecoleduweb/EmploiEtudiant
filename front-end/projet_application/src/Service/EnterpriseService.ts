import type { Enterprise } from "../Models/Enterprise"
import { GET } from "../ts/server"

const fetchAllEnterprises = async () => {
  const response = await GET<any>("/enterprise/all")
  return response.map((e: Enterprise) => {
    return { label: e.name, value: e.id }
  })
}

export default fetchAllEnterprises