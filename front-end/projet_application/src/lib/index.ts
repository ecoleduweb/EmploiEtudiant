// place files you want to import through the `$lib` alias in this folder.
import { writable } from "svelte/store";
import type { StudyProgram } from "../Models/StudyProgram";


export const isLoggedIn = writable(false);
export const currentUser = writable();
export const studyPrograms = writable<Option[]>([]);

export interface Option { label: string; value: number; }
export interface studyProgramModalSettings {
    mode: number, //0 = Create, 1 = Edit
    studyProgram: Option | undefined, //StudyProgram selected (Only in edit mode)
}