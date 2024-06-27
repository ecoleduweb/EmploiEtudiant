import { city } from "$lib";
import { GET } from "../ts/server";

const getCityData = async () => {
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
    let subscribedCity: any;

    city.subscribe((c) => { subscribedCity = c })

    if (subscribedCity) {
      cityData = subscribedCity
    }
    else if (savedData) {
      cityData = JSON.parse(savedData)
    }
  }
  catch {
    cityData = getCityData()
    city.set(cityData)
    localStorage.setItem("City", JSON.stringify(cityData))
  }

  finally {
    return cityData.cities
  }
}

const fetchCity = async () => {
  console.log("Fetching cities...")

  return cacheCity()
}

export default fetchCity;