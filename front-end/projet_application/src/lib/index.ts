// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";

export const maxTimeBeforeRefresh = 259200 //3 jours en secondes.

export interface Option { label: string; value: number; }

export interface City {
    cities: Array<Option>,
    cachingDate: number,
    expiringDate: number
}

export const isLoggedIn = writable(false);
export const currentUser = writable();
export const studyPrograms = writable<StudyProgram[]>([]);
export const city = writable<City>({
    cities: [],
    cachingDate: 0,
    expiringDate: 0
});
