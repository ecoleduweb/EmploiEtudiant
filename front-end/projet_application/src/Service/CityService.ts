import type { City } from "$lib/interfaces";
import { GET } from "../ts/server";

let city: City;
let citiesMap: Map<number, string> = new Map()

const getCityData = async (): Promise<City> => {
  const response = await GET<any>("/city/all")

  let cities = response.map((c: any) => {
    return { label: c.city, value: c.id }
  })


  citiesMap = new Map(cities.map((c: any) => [c.value, c.label]))

  return {
    cities: cities,
    cachingDate: new Date().getTime(),
  }
}

const cacheCity = async () => {
  let savedData = localStorage.getItem("City")
  let cityData: any;

  try {
    if (city.cachingDate !== 0) {
      cityData = city
    }
    else if (savedData) {
      cityData = JSON.parse(savedData)

      citiesMap = new Map(cityData.cities.map((c: any) => [c.value, c.label]))
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
  return citiesMap.get(cityId) || ""
}

export default fetchCity;