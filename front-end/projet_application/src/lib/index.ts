// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";
import type { User } from "../Models/User";


export const isLoggedIn = writable(false);
export const currentUser = writable<User | undefined>();
export const studyPrograms = writable<StudyProgram[]>([]);