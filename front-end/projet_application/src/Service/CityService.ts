import type { City } from "../Models/City";
import type { Option } from "../Models/Option";
import { GET } from "../ts/server";

const getCities = async (): Promise<City[]> => {
  let cityData: any;

  try {
    const savedData = localStorage.getItem("City")
    if (savedData) {
      cityData = JSON.parse(savedData)
    }
    // Valeur de date hardcodée. Pas parfait, mais plus simple.
    if (cityData?.cachingDate && cityData.cachingDate > new Date("2026-05-28").getTime()) {
      return cityData.cities
    }

    // pas de ville à retourner? Alors on les fetchs.
    const cities = await GET<City[]>("/city/all")
    cityData = {
      cities: cities,
      cachingDate: new Date().getTime(),
    }
    localStorage.setItem("City", JSON.stringify(cityData))
    return cityData.cities
  }
  catch {
    console.error("Failed to fetch cities. Returning empty array.")
    alert("Impossible de récupérer les villes. Veuillez contacter le service des communications pour nous faire part du problème.")
  }
  // plan b
  finally {
    return cityData.cities ? cityData.cities : GET<City[]>("/city/all")
  }
}

export const fetchCitiesAsOptions = async (): Promise<Option[]> => {
  const cities = await getCities();
  return cities.map((x: City) => ({ value: x.id, label: x.city }));
}

export const fetchCities = async (): Promise<City[]> => {
  return getCities()
}

export const getCityNameById = async (cityId: number): Promise<string> => {
  const cities = await getCities();
  return cities.find((c: any) => c.id === cityId)?.city ?? "Ville inconnue";
}
