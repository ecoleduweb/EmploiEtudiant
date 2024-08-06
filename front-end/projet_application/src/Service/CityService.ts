import type { City } from "$lib/interfaces";
import { GET } from "../ts/server";

let city: City;

const getCityData = async (): Promise<City> => {
  const response = await GET<any>("/city/all")

  let cities = response.map((c: any) => {
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
    if (city.cachingDate !== 0) {
      cityData = city
    }
    else if (savedData) {
      cityData = JSON.parse(savedData)
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

export default fetchCity;