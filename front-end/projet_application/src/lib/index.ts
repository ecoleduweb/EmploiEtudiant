// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";

export const isLoggedIn = writable(false);
export const currentUser = writable();
export const studyPrograms = writable<StudyProgram[]>([]);