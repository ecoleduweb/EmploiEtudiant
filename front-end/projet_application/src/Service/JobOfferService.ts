import { InvalidDataError } from "../CustomError/invalidDataError"
import type { JobOffer } from "../Models/Offre"
import { DELETE, GET, POST, PUT } from "../ts/server"

export const fetchJobOffers = async (): Promise<JobOffer[]> => {
  return await GET<JobOffer[]>("/jobOffer/all")
}

export const fetchJobOffer = async (id: number): Promise<JobOffer> => {
  const jobOffer = await GET<JobOffer>(`/jobOffer/${id}`, false)
  return prepareJobOffer(jobOffer)
}

export const fetchJobOffersByEmployer = async (): Promise<JobOffer[]> => {
  let jobOffers = await GET<JobOffer[]>(
    "/jobOffer/employer/all?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true",
  )
  return prepareJobOffers(jobOffers)
}

export const fetchApprovedJobOffers = async (): Promise<JobOffer[]> => {
  let jobOffers = await GET<JobOffer[]>(
    "/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true",
  )
  return prepareJobOffers(jobOffers)
}

const prepareJobOffer = (jobOffer: JobOffer) => {
  if (jobOffer.lastModifiedDate) jobOffer.lastModifiedDate = new Date(jobOffer.lastModifiedDate)
  return jobOffer
}
const prepareJobOffers = (jobOffers: JobOffer[] = []) => {
  return jobOffers.map(prepareJobOffer)
}

export const upsertJobOffer = async (jobOffer: JobOffer): Promise<[JobOffer | null, any]> => {
  try {
    const payload: JobOffer = {
      ...jobOffer,
      dateEntryOffice: jobOffer.dateEntryOffice ? new Date(jobOffer.dateEntryOffice).toISOString() : null,
      offerDebut: jobOffer.offerDebut ? new Date(jobOffer.offerDebut).toISOString() : null,
      deadlineApply: jobOffer.deadlineApply ? new Date(jobOffer.deadlineApply).toISOString() : null,
      approvedDate: jobOffer.approvedDate ? new Date(jobOffer.approvedDate).toISOString() : null,
      last_modified_by_id: jobOffer.last_modified_by_id ?? null,
      lastModifiedDate: jobOffer.lastModifiedDate ? new Date(jobOffer.lastModifiedDate).toISOString() : null,
    } as any
    const response = jobOffer.id ?
      await PUT<JobOffer, JobOffer>(
        `/jobOffer/${jobOffer.id}`,
        payload,
      )
      :
      await POST<JobOffer, JobOffer>(
        "/jobOffer/new",
        payload,
      )
    return [response.data, null]
  } catch (err: any) {
    if (err instanceof InvalidDataError) {
      return [null, { [err.field]: err.message }]
    } else {
      console.error("Not Invalid data error", err)
    }
  }
  return [null, null]
}

export const approveJobOffer = async (offerId: number, isApproved: boolean, approbationMessage: string, enterpriseId?: number): Promise<JobOffer> => {
  try {
    const payload = {
      id: offerId,
      selectedEnterpriseId: enterpriseId,
      approbationMessage: approbationMessage,
      isApproved: isApproved,
    }
    const response = await PUT<any, any>(`/jobOffer/approve/${offerId}`, payload)
    return response.data
  } catch (error) {
    console.error("Erreur lors de l'approbation", error)
    alert(
      "Une erreur est survenue lors de l'approbation de l'offre. Veuillez réessayer ou contacter le support si le problème persiste.",
    )
    return null as any
  }
}

export const toggleArchive = async (offerId: number): Promise<JobOffer> => {
  try {
    const response = await POST<any, any>(`/jobOffer/archive/${offerId}`, {})
    return response.data
  } catch (error) {
    console.error("Erreur lors de la modification de l'état d'archivage", error)
    alert(
      "Une erreur est survenue lors de la modification de l'état d'archivage de l'offre. Veuillez réessayer ou contacter le support si le problème persiste.",
    )
    return null as any
  }
}

export const deleteJobOffer = async (offerId: number): Promise<void> => {
  try {
    await DELETE(`/jobOffer/${offerId}`)
  } catch (error) {
    console.error("Erreur lors de la suppression de l'offre", error)
    alert(
      "Une erreur est survenue lors de la suppression de l'offre. Veuillez réessayer ou contacter le support si le problème persiste.",
    )
  }
}