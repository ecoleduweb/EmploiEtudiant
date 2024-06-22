from app import db
from app.models.offer_program_model import OfferProgram

class OfferProgramRepo:
    def linkOfferProgram(self, programId, offerId):
        new_offer_program = OfferProgram(programId=programId, offerId=offerId)
        db.session.add(new_offer_program)
        db.session.commit()
        return new_offer_program

    def getProgramIdByOfferId(self, offerId):
        offerPrograms = OfferProgram.query.filter_by(offerId=offerId).all()
        if offerPrograms:
            return [offerProgram.id for offerProgram in offerPrograms]
        else:
            return []
        
    def updateOfferProgram(self, offerId, programIds):
        offerPrograms = OfferProgram.query.filter_by(offerId=offerId).all()  
        for offerProgram in offerPrograms:
            if offerProgram.programId not in programIds:
                db.session.delete(offerProgram)
        for programId in programIds:
            offerProgram = OfferProgram.query.filter_by(offerId=offerId, programId=programId).first()
            if not offerProgram:
                offerProgram = OfferProgram(offerId=offerId, programId=programId)
                db.session.add(offerProgram)
        db.session.commit()