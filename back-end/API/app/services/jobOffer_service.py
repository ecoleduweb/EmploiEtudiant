import os
from app.repositories.jobOffer_repo import JobOfferRepo
from app.repositories.enterprise_repo import EnterpriseRepo
from app.repositories.study_program_repo import StudyProgramRepo
from app.repositories.user_repo import UserRepo
from datetime import datetime, timezone
from app.services.user_service import UserService
from app.customexception.exception import ValidationException, NotFoundException , PermissionException
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.services.email_service import send_mail
from app.dtos.job_offer_dto import (
    JobOfferReadDTO,
    JobOfferCreateDTO,
    JobOfferUpdateDTO,
    JobOfferApproveDTO
)
from app.utils.SanitizeDOM import sanitize_html

employment_schedule_service = EmploymentScheduleService()
job_offer_repo = JobOfferRepo()
user_service = UserService()
enterprise_repo = EnterpriseRepo()
studyProgram_repo = StudyProgramRepo()
user_repo = UserRepo()

class JobOfferService:

    def all(self, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details) -> list[JobOfferReadDTO]:
        return job_offer_repo.all(needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)
    
    def create(self, current_user, dto: JobOfferCreateDTO) -> JobOfferReadDTO:
        enterprise = None
        if current_user.isModerator:
            enterprise = enterprise_repo.find_by_id(dto.enterpriseId) # Just to throw is it is not found
            dto.isApproved = True
            dto.approvedDate = datetime.now(timezone.utc)
        else:
            dto.isApproved = None
            # Quand un employeur crée pour la première fois une offre, on crée aussi son entreprise.
            if current_user.enterpriseId == None:
                enterprise = enterprise_repo.create(dto.enterprise)
                user_repo.update_enterprise_id(current_user.id, enterprise.id)
            else:
                enterprise = enterprise_repo.find_by_id(current_user.enterpriseId)
            dto.enterpriseId = enterprise.id

        dto.description = sanitize_html(dto.description)
        dto.title = sanitize_html(dto.title)
        dto.last_modified_by_id = current_user.id
        dto.lastModifiedDate = datetime.now(timezone.utc)
        job_offer = job_offer_repo.create(dto)
        if not current_user.isModerator:
            send_mail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Création d'une nouvelle offre d'emploi", "Une nouvelle offre d'emploi a été créée du nom de <b>" + job_offer.title + "</b> par <b>" + current_user.firstName + "</b> <b>" + current_user.lastName + "</b>, pour l'entreprise " + enterprise.name + ".")
            send_mail(current_user.email, "Accusé de réception - Création d'une nouvelle offre d'emploi", "Votre offre d'emploi (<b>" + job_offer.title + "</b>) a bien été créée. Celle-ci sera affichée publiquement lorsqu'elle sera approuvée. <br> Veuillez prévoir un délai moyen de 24 à 48 heures ouvrables. <br>Vous recevrez un courriel lorsque votre offre sera affichée sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. <br><br>Merci d'avoir soumis votre offre!")
        return job_offer

    def delete_by_id(self, current_user, id) -> JobOfferReadDTO:
        dto = job_offer_repo.find_by_id(id, False, False, False)
        
        if not current_user.isModerator and current_user.enterpriseId != dto.enterpriseId:
            raise PermissionException("Impossible de supprimer une offre qui ne vous appartient pas")

        job_offer_repo.delete_by_id(id)

        if current_user.isModerator and dto.last_modified_by_id is current_user.id:
            send_mail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Suppression d'une offre d'emploi", f"L'offre d'emploi au nom de <b> {dto.title} </b> en attente d'approbation a été supprimée par l'administrateur.")
        return dto
    
    def find_enterprises_job_offer_by_user_id(self, user_id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details) -> list[JobOfferReadDTO]:
        return job_offer_repo.find_enterprises_job_offer_by_user_id(user_id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)
    
    def update(self, current_user, dto) -> JobOfferReadDTO:
        if not current_user.isModerator and current_user.enterpriseId != dto.enterpriseId: # Peut pas utiliser une autre entreprise que la sienne
            raise PermissionException("Impossible de mettre à jour une offre qui ne vous appartient pas")

        job_offer_to_udpate = self.find_by_id(dto.id, True, True, True)
        if not current_user.isModerator and current_user.enterpriseId != job_offer_to_udpate.enterpriseId: # Ne peut pas transférer une offre à une autre entreprise que la sienne
            raise PermissionException("Impossible de mettre à jour une offre qui ne vous appartient pas")
        enterprise_repo.find_by_id(dto.enterpriseId) # Just to throw if the enterprise is not found

        if not current_user.isModerator:
            
            if(self._job_offer_was_modified_from_original(job_offer_to_udpate, dto)):
                dto.isApproved = None
                dto.approbationMessage = None
            else:
                dto.isApproved = job_offer_to_udpate.isApproved # Si l'offre n'est pas modifiée, on garde l'ancien statut.

        dto.description = sanitize_html(dto.description)
        dto.title = sanitize_html(dto.title)
        dto.last_modified_by_id = current_user.id
        dto.lastModifiedDate = datetime.now(timezone.utc)
        updated = job_offer_repo.update_job_offer(dto)

        if job_offer_to_udpate.isApproved != dto.isApproved and dto.isApproved == None and not current_user.isModerator:
            send_mail(current_user.email, "Modification d'une offre d'emploi", f"L'offre d'emploi au nom de <b> {dto.title} </b> a été modifiée avec succès. <br> Veuillez prévoir un délai moyen de 24 à 48 heures ouvrables pour la mise à jour de votre offre. <br> Vous recevrez un courriel lorsque votre offre modifiée sera affichée sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. ")
            send_mail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Modification d'une offre d'emploi", f" {current_user.firstName} {current_user.lastName} a modifié son offre d'emploi <b>" + dto.title + "</b> et est en attente d'approbation.")
        return updated

    def find_by_id(self, id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details) -> JobOfferReadDTO:
        return job_offer_repo.find_by_id(id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)

    def get_all(self, get_entreprise_details, employment_schedule_details, study_program_details) -> list[JobOfferReadDTO]:
        return job_offer_repo.all_availables(get_entreprise_details, employment_schedule_details, study_program_details)
    
    def approve(self, dto: JobOfferApproveDTO) -> JobOfferReadDTO:
        job_offer_to_approve = job_offer_repo.find_by_id(dto.id, True, False, False)
        previous_enterprise_id = job_offer_to_approve.enterpriseId
        user_that_created_the_job_offer = user_repo.find_by_id(job_offer_to_approve.last_modified_by_id)
        job_offer_to_approve.isApproved = dto.isApproved
        # Only setting the enterpriseId when the offer is approved
        if dto.isApproved:
            job_offer_to_approve.enterpriseId = dto.selectedEnterpriseId
        job_offer_to_approve.approbationMessage = dto.approbationMessage
        job_offer_to_approve.approvedDate = datetime.now(timezone.utc)
        updated = job_offer_repo.update_job_offer(job_offer_to_approve)
        
        ## Si on approuve l'offre, on approuve aussi l'entreprise (au besoin: si l'entreprise n'est pas déja approuvée dans une autre offre d'emploi antérieure)
        if not user_that_created_the_job_offer.isModerator:
            if dto.isApproved:
                user_service.manage_temporary_enterprise(dto.selectedEnterpriseId, previous_enterprise_id)
                send_mail(user_that_created_the_job_offer.email, "Approbation d'une offre d'emploi", f"""L'offre d'emploi au nom de <b>{job_offer_to_approve.title}</b> a été approuvée.<br>
                            Elle est maintenant affichée publiquement sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. 
                            <br>{f'{job_offer_to_approve.approbationMessage}<br>' if job_offer_to_approve.approbationMessage else ''}
                            <br><br>Merci d'avoir soumis votre offre!""")
            else:
                send_mail(user_that_created_the_job_offer.email, "Refus de l'approbation de l'offre d'emploi", f"L'offre d'emploi au nom de <b>{job_offer_to_approve.title}</b> a été refusée.<br> Raison: {job_offer_to_approve.approbationMessage}")
        return updated

    def archive(self, id):
        if job_offer_repo.jobOfferExist(id):
            job_offer_repo.archiveJobOffer(id)
        else:
            raise NotFoundException("Job offer not found", id)
    
    def _job_offer_was_modified_from_original(self, original_job_offer: JobOfferReadDTO, updated_job_offer: JobOfferUpdateDTO):
        # Vérifier si le titre ou la description d'une offre a changé
        if original_job_offer.title != updated_job_offer.title or original_job_offer.description != updated_job_offer.description:
            return True
        
        if not original_job_offer.isApproved and (original_job_offer.title != updated_job_offer.title
                                        or original_job_offer.description != updated_job_offer.description 
                                        or original_job_offer.offerDebut != updated_job_offer.offerDebut 
                                        or original_job_offer.address != updated_job_offer.address 
                                        or original_job_offer.dateEntryOffice != updated_job_offer.dateEntryOffice 
                                        or original_job_offer.deadlineApply != updated_job_offer.deadlineApply
                                        or original_job_offer.email != updated_job_offer.email
                                        or original_job_offer.hoursPerWeek != updated_job_offer.hoursPerWeek
                                        or original_job_offer.offerLink != updated_job_offer.offerLink
                                        or original_job_offer.salary != updated_job_offer.salary
                                        ):
            return True