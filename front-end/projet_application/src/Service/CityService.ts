import type { City } from "$lib/interfaces";
import { GET } from "../ts/server";

let city: City | null = null;


const getCityData = async (): Promise<City> => {
  const response = await GET<any>("/city/all")

  const cities = response.map((c: any) => {
    return { label: c.city, value: c.id }
  })

  return {
    cities: cities,
    cachingDate: new Date().getTime(),
  }
}

const cacheCity = async () => {
  let savedData = localStorage.getItem("City")
  let cityData: any = { cities: [] };

  try {
    if (city && city.cachingDate !== 0) {
      cityData = city
    }
    else if (savedData) {
      try {
        cityData = JSON.parse(savedData)
      } catch {
        cityData = await getCityData()
        city = cityData
        localStorage.setItem("City", JSON.stringify(cityData))
      }
    }
    else {
      cityData = await getCityData()
      city = cityData
      localStorage.setItem("City", JSON.stringify(cityData))
    }
  }
  catch (error) {
    console.error("Error fetching cities:", error)
    cityData = { cities: [] }
  }

  return cityData?.cities || []
}

const fetchCity = async () => {
  return cacheCity()
}

export const getCityName = async (cityId: number): Promise<string> => {
  const cities = await fetchCity();
  const city = cities.find((c: any) => c.value === cityId);
  return city ? city.label : "Unknown City";
}

export default fetchCity;