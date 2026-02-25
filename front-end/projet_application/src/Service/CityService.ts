import type { City } from "$lib/interfaces";
import { GET } from "../ts/server";

let city: City;
let cities: any[] = []

const getCityData = async (): Promise<City> => {
  const response = await GET<any>("/city/all")

  cities = response.map((c: any) => {
    return { label: c.city, value: c.id }
  })

  return {
    cities: cities,
    cachingDate: new Date().getTime(),
  }
}

const cacheCity = async () => {
  let savedData = localStorage.getItem("City")
  let cityData: any;

  try {
    if (city && city.cachingDate !== 0) {
      cityData = city
      cities = cityData.cities
    }
    else if (savedData) {
      cityData = JSON.parse(savedData)
      cities = cityData.cities
    }
  }
  catch {
    cityData = await getCityData()
    city = cityData
    localStorage.setItem("City", JSON.stringify(cityData))
  }

  finally {
    return cityData.cities
  }
}

const fetchCity = async () => {
  return cacheCity()
}

export const getCityName = (cityId: number): string => {
  const foundCity = cities.find((c: any) => c.value === cityId)
  return foundCity ? foundCity.label : "Unknown"
}

export default fetchCity;