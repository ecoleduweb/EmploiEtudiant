export interface jobOffer { 
    id: number; // id de l'offre
    title: string; // titre de l'offre
    address: string; // lieu de travail
    description: string; // description de l'offre
    offerDebut: string // date d'affichage de l'offre
    dateEntryOffice: string; // date d'entrée au bureau
    deadlineApply: string // date limite pour postuler
    email: string; // courriel de la personne à contacter
    hoursPerWeek: number; // nombre d'heures par semaine  
    compliantEmployer: boolean; // employeur conciliant ou non
    internship: boolean; // si l'offre est un stage
    offerLink: string; // lien vers l'offre ou site web de l'employeur
    offerStatus: number;
    active: boolean; // si l'offre est active ou non
    salary: string; // salaire de lheure                     ** A AJOUTER BD **
    scheduleId: number; // id de l'horaire de travail
    employerId: number; // id de l'employeur 
    isApproved: boolean | null; // si l'offre est approuvée ou non
    approbationMessage: string | null; // message d'approbation
}