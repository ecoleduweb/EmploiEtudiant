from app import db
from app.models.job_offer_model import JobOffer
from app.models.employment_schedule_model import EmploymentSchedule
from app.models.study_program_model import StudyProgram
from app.models.user_model import User
from app.customexception.exception import NotFoundException
from datetime import date, timedelta, datetime, timezone
from app.dtos.job_offer_dto import (
    JobOfferReadDTO,
    JobOfferCreateDTO,
    JobOfferUpdateDTO
)

class JobOfferRepo:

    def create(self, dto: JobOfferCreateDTO) -> JobOfferReadDTO:
        job_offer = JobOffer(**dto.model_dump(exclude={"studyPrograms", "employmentSchedules", "enterprise"}))
        db.session.add(job_offer)
        self._set_study_programs_to_model(job_offer, [sp.id for sp in dto.studyPrograms])
        self._set_employment_schedules_to_model(job_offer, [es.id for es in dto.employmentSchedules])
        db.session.commit()
        return JobOfferReadDTO.model_validate(job_offer)

    def _set_study_programs_to_model(self, newJobOffer, study_program_ids: list[int]) -> None:
        programs = db.session.scalars(
            db.select(StudyProgram).where(StudyProgram.id.in_(study_program_ids))
        ).all()
        newJobOffer.studyPrograms = programs

    def _set_employment_schedules_to_model(self, newJobOffer, schedule_ids: list[int]) -> None:
        schedules = db.session.scalars(
            db.select(EmploymentSchedule).where(EmploymentSchedule.id.in_(schedule_ids))
        ).all()
        newJobOffer.employmentSchedules = schedules

    def delete_by_id(self, id) -> None:
        job_offer = JobOffer.query.filter_by(id=id).first()
        if job_offer is None:
            raise NotFoundException("Job offer not found", id)
        db.session.delete(job_offer)
        db.session.commit()

    def find_enterprises_job_offer_by_user_id(self, user_id, get_entreprise_details, employment_schedule_details, study_program_details) -> list[JobOfferReadDTO]:
        user = db.session.get(User, user_id)
        if user is None or user.enterpriseId is None:
            raise NotFoundException("User or user's enterprise not found", user_id)
        
        query = JobOffer.query.filter_by(enterpriseId=user.enterpriseId)
        job_offers = self._load_job_offer_relations(get_entreprise_details, employment_schedule_details, study_program_details, query)
        return [JobOfferReadDTO.model_validate(job_offer) for job_offer in job_offers]

    def update_job_offer(self, dto: JobOfferUpdateDTO) -> JobOfferReadDTO:
        job_offer = JobOffer.query.filter_by(id=dto.id).first()
        if job_offer is None:
            raise NotFoundException("Job offer not found", dto.id)
        job_offer.title = dto.title
        job_offer.description = dto.description
        job_offer.address = dto.address
        job_offer.offerDebut = dto.offerDebut
        job_offer.dateEntryOffice = dto.dateEntryOffice
        job_offer.deadlineApply = dto.deadlineApply
        job_offer.email = dto.email
        job_offer.hoursPerWeek = dto.hoursPerWeek
        job_offer.offerLink = dto.offerLink
        job_offer.salary = dto.salary
        job_offer.enterpriseId = dto.enterpriseId
        job_offer.lastModifiedDate  = datetime.now(timezone.utc)
        job_offer.isApproved = dto.isApproved
        job_offer.approbationMessage = dto.approbationMessage 
        job_offer.last_modified_by_id = dto.last_modified_by_id
        
        self._set_study_programs_to_model(job_offer, [sp.id for sp in dto.studyPrograms])
        self._set_employment_schedules_to_model(job_offer, [es.id for es in dto.employmentSchedules])

        db.session.commit()
        return self.find_by_id(dto.id, True, True, True)

    def find_by_id(self,id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details) -> JobOfferReadDTO:
        query = JobOffer.query.filter_by(id=id)
        job_offers = self._load_job_offer_relations(needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details, query)
        job_offer = job_offers[0] if job_offers else None
        if job_offer is None:
            raise NotFoundException("Job offer not found", id)
        return JobOfferReadDTO.model_validate(job_offer)

    def all(self, get_entreprise_details, employment_schedule_details, study_program_details) -> list[JobOfferReadDTO]:
        job_offers = self._load_job_offer_relations(get_entreprise_details, employment_schedule_details, study_program_details, JobOffer.query)
        dtos = [JobOfferReadDTO.model_validate(jo) for jo in job_offers]
        return dtos
    
    def all_availables(self, get_entreprise_details, employment_schedule_details, study_program_details) -> list[JobOfferReadDTO]:
        today = datetime.now(timezone.utc).date()
        statement = JobOffer.query.filter(
            JobOffer.isApproved == True,
            JobOffer.offerDebut <= today,
            JobOffer.deadlineApply >= today
        ).order_by(JobOffer.approvedDate.desc())
        job_offers = self._load_job_offer_relations(get_entreprise_details, employment_schedule_details, study_program_details, statement)
        dtos = [JobOfferReadDTO.model_validate(jo) for jo in job_offers]
        return dtos

    def _load_job_offer_relations(self, get_entreprise_details, employment_schedule_details, study_program_details, statement):
        if get_entreprise_details:
            statement = statement.options(db.joinedload(JobOffer.enterprise))
        else:
            statement = statement.options(db.noload(JobOffer.enterprise))
        if employment_schedule_details:
            statement = statement.options(db.joinedload(JobOffer.employmentSchedules))
        else: 
            statement = statement.options(db.noload(JobOffer.employmentSchedules))
        if study_program_details:
            statement = statement.options(db.joinedload(JobOffer.studyPrograms))
        else:
            statement = statement.options(db.noload(JobOffer.studyPrograms))
        job_offers = statement.all()
        return job_offers

    def update_approve_by_id(self, id, isApproved, approbationMessage):
        job_offer = JobOffer.query.filter_by(id=id).first()
        if job_offer is None:
            raise NotFoundException("Job offer not found", id)
        job_offer.isApproved = isApproved
        job_offer.approbationMessage = approbationMessage
        if job_offer.isApproved:
            job_offer.approvedDate = datetime.now(timezone.utc)
        db.session.commit()

    def archiveJobOffer(self, id):
        job_offer = JobOffer.query.filter_by(id=id).first()
        job_offer.deadlineApply = date.today() - timedelta(days=1)
        db.session.commit()
        return JobOfferReadDTO.model_validate(job_offer)

    def jobOfferExist(self, id):
        return JobOffer.query.filter_by(id=id).first() is not None
    
    def find_study_program_ids_by_offer_id(self,id) -> list[int]:
        job_offer = JobOffer.query.filter_by(id=id).first()
        if job_offer is None:
            raise NotFoundException("Job offer not found", id)
        return [program.id for program in job_offer.studyPrograms]
    
    def find_employment_schedules_by_offer_id(self, id) -> list[EmploymentSchedule]:
        job_offer = JobOffer.query.filter_by(id=id).first()
        if job_offer is None:
            raise NotFoundException("Job offer not found", id)
        return job_offer.employmentSchedules