from app.repositories.offer_programm_repo import OfferProgramRepo
offer_program_repo = OfferProgramRepo()

class OfferProgramService:
    def linkOfferProgram(self, programId, offerId):
        return offer_program_repo.linkOfferProgram(programId, offerId)