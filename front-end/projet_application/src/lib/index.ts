// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";
import type { User } from "../Models/User";
import type { Enterprise } from "../Models/Enterprise";


export const isLoggedIn = writable(false);
export const currentUser = writable<User | undefined>();
export const studyPrograms = writable<StudyProgram[]>([]);
export const enterprises = writable<Enterprise[]>([]);