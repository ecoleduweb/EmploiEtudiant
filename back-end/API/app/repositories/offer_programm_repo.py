from app import db
from app.models.offer_programm_model import OfferProgram

class OfferProgramRepo:
    def linkOfferProgram(self, programId, offerId):
        new_offer_program = OfferProgram(programId=programId, offerId=offerId)
        db.session.add(new_offer_program)
        db.session.commit()
        return new_offer_program
