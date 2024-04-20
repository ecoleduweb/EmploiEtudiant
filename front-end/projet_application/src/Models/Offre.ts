export interface jobOffer { 
    title: string; // titre de l'offre
    address: string; // lieu de travail
    // EVENTUELLEMENT, UTILISER LA SECTION VILLE DE C-A
    description: string; // description de l'offre
    dateEntryOffice: string // date d'entrée en fonction
    deadlineApply: string // date limite pour postuler
    email: string; // courriel de la personne à contacter
    hoursPerWeek: string; // nombre d'heures par semaine  
    compliantEmployer: boolean; // employeur conciliant ou non
    internship: boolean; // si l'offre est un stage
    offerLink: string; // lien vers l'offre ou site web de l'employeur
    offerStatus: number;
    urgent: boolean; // si l'offre est urgente
    active: boolean; // si l'offre est active ou non
    salary: string; // salaire de lheure                     ** A AJOUTER BD **
    scheduleId: number; // id de l'horaire de travail
    employerId: number; // id de l'employeur (pas encore inclus)
    isApproved: boolean; // si l'offre est approuvée ou non
} 