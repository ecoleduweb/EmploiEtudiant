import type { Enterprise } from "./Enterprise"
import type { EmploymentSchedule } from "./EmploymentSchedule"
import type { StudyProgram } from "./StudyProgram"

export interface JobOffer {
    studyPrograms: StudyProgram[]
    employmentSchedules: EmploymentSchedule[]
    id: number // id de l'offre
    title: string // titre de l'offre
    address: string // lieu de travail
    description: string // description de l'offre
    offerDebut: string // date d'affichage de l'offre
    dateEntryOffice: string // date d'entrée au bureau
    deadlineApply: string // date limite pour postuler
    email: string // courriel de la personne à contacter
    hoursPerWeek: number // nombre d'heures par semaine
    internship: boolean // si l'offre est un stage
    offerLink: string // lien vers l'offre ou site web de l'employeur
    offerStatus: number
    salary: string
    enterpriseId?: number
    isApproved: boolean | null // si l'offre est approuvée ou non
    approbationMessage: string | null // message d'approbation
    acceptCondition: boolean | null | undefined
    approvedDate: string
    enterprise?: Enterprise
    lastModifiedDate?: Date
    last_modified_by_id?: number
}
