import { GET } from "../ts/server";

const fetchCity = async () => {
  const response = await GET<any>("/city/all")
  return response.map((v: any) => {
    return { label: v.city, value: v.id }
  })
}

export default fetchCity;