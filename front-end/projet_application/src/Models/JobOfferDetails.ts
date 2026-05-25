import type { Enterprise } from './Enterprise'
import type { JobOffer } from './Offre'
import type { StudyProgram } from './StudyProgram'
export interface JobOfferDetails extends JobOffer {
    enterprise: Enterprise | null
    studyPrograms: StudyProgram[] | null
    employementSchedules: { id: string, description: string }[] | null
    lastModifiedDate: string // Date de la dernière modification de l'offre
}
