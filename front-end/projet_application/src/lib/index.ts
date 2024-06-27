// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";
import type { City } from "./interfaces";

export const isLoggedIn = writable(false);
export const currentUser = writable();
export const studyPrograms = writable<StudyProgram[]>([]);
export const city = writable<City>({
    cities: [],
    cachingDate: 0
});
