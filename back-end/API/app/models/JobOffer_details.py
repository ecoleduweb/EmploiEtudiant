class JobOfferDetails:
    def __init__(self, jobOffer):
        self.id = jobOffer.id
        self.title = jobOffer.title
        self.address = jobOffer.address
        self.description = jobOffer.description
        self.offerDebut = jobOffer.offerDebut
        self.dateEntryOffice = jobOffer.dateEntryOffice
        self.deadlineApply = jobOffer.deadlineApply
        self.email = jobOffer.email
        self.hoursPerWeek = jobOffer.hoursPerWeek
        self.offerLink = jobOffer.offerLink
        self.salary = jobOffer.salary
        self.active = jobOffer.active
        self.approbationMessage = jobOffer.approbationMessage
        self.employerId = jobOffer.employerId
        self.scheduleId = jobOffer.scheduleId
        self.isApproved = jobOffer.isApproved
        self.approvedDate = jobOffer.approvedDate
        self.enterprise = None

    def AddEnterprise(self, enterprise):
        self.enterprise = enterprise

    def to_json_string(self):
        json =  {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'description': self.description,
            'offerDebut': str(self.offerDebut),
            'dateEntryOffice': str(self.dateEntryOffice),  # Convert datetime to string
            'deadlineApply': str(self.deadlineApply),  # Convert date to string
            'email': self.email,
            'hoursPerWeek': self.hoursPerWeek,
            'offerLink': self.offerLink,
            'salary': self.salary,
            'active': self.active,
            'approbationMessage': self.approbationMessage,
            'employerId': self.employerId,
            'isApproved': self.isApproved,
            'approvedDate': self.approvedDate
        }

        if self.enterprise != None : 
            json['enterprise'] = {
                'name': self.enterprise.name
            }

        # si jamais on a une liste, faire une boucle for pour ajouter les infos dans le json

        return json