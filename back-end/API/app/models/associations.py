from app import db
   
job_offer_study_program = db.Table(
    "offer_program",
    db.Column("offerId", db.Integer, db.ForeignKey("job_offer.id", ondelete="CASCADE"), primary_key=True),
    db.Column("programId", db.Integer, db.ForeignKey("study_program.id", ondelete="CASCADE"), primary_key=True),
)

job_offer_employment_schedule = db.Table(
    "offer_schedule",
    db.Column("offerId", db.Integer, db.ForeignKey("job_offer.id", ondelete="CASCADE"), primary_key=True),
    db.Column("employmentScheduleId", db.Integer, db.ForeignKey("employment_schedule.id", ondelete="CASCADE"), primary_key=True),
)