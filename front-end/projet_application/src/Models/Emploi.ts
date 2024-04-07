export interface Emploi {
    id: number;
    title: string;
    address: string;
    description: string;
    dateEntryOffice: string;
    deadlineApply: string;
    email: string;
    hoursPerWeek: number;
    compliantEmployer: boolean;
    internship: boolean;
    offerStatus: number;
    offerLink: string;
    urgent: boolean;
    active: boolean;
    employerId: number;
    scheduleId: number;
}
