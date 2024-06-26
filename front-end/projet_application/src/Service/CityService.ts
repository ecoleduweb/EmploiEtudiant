import { city } from "$lib";
import { GET } from "../ts/server";


const fetchCity = async () => {
  console.log("Fetching cities...")

  const response = await GET<any>("/city/all")

  let cities = response.map((v: any) => {
    return { label: v.city, value: v.id }
  })

  let Data = {
    cities: cities,
    cachingDate: new Date().getTime(),
    expiringDate: new Date().setDate(new Date().getDate() + 3)
  }

  city.set(Data)

  localStorage.setItem("city", JSON.stringify(Data))

  return cities
}

export default fetchCity;