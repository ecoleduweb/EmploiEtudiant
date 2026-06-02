import type { StudyProgram } from "../Models/StudyProgram"
import type { Option } from "../Models/Option"
import { GET } from "../ts/server"

export const fetchStudyPrograms = async (): Promise<StudyProgram[]> => {
  return await GET<StudyProgram[]>("/studyProgram/all")
}

export const fetchStudyProgramsAsOptions = async (): Promise<Option[]> => {
  const programs = await fetchStudyPrograms()
  return programs.map((program) => ({
    value: program.id,
    label: program.name,
  }))
}