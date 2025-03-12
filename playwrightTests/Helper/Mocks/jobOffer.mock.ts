import { MockConfig } from "../types";
export const jobOfferMocks = {
    jobOfferNew: {
        url: '*/**/jobOffer/new',
        response: {
            status: 200,
            json: { "message": "Offre créée" }
        }
    },
    jobOfferEmployer: {
        url: '*/**/jobOffer/employer/*',
        response: {
            status: 404,
            json: { "message": "Offres non trouvées" }
        }
    },
    jobOfferVerifyURL: {
        url: '*/**/jobOffer/verifyURL',
        response: {
            status: 200,
            json: {
                message: "URL is accessible"
            }
        }
    },

    jobOfferNewInvalidHour: {
        url: '*/**/jobOffer/new',
        response: {
            status: 400,
            json: {
                field: "hoursPerWeek",
                message: "Ce champ doit correspondre a un nombre."
            }
        }
    },

    jobOfferNewInvalid: {
        url: '*/**/jobOffer/new',
        response: {
            status: 400,
            json: {
                field: "title",
                message: "Ceci est un retour pour tester les erreurs back-end pour ajouter."
            }
        }
    },

    jobOfferNewOffer: {
        url: '*/**/jobOffer/employer/*',
        response: {
            status: 200,
            json: [{
                "active": true,
                "address": "123 rue bacon",
                "approbationMessage": "\ud83e\udd96",
                "lastModifiedDate": new Date().toISOString().split('T')[0],
                "approvedDate": new Date().toISOString().split('T')[0],
                "dateEntryOffice": (() => {
                    const date = new Date();
                    date.setDate(date.getDate() + 1);
                    return date.toISOString().split('T')[0];
                })(),
                "deadlineApply": (() => {
                    const date = new Date();
                    date.setDate(date.getDate() + 1);
                    return date.toISOString().split('T')[0];
                })(),
                "description": "\ud83e\udd96",
                "email": "bob@cegeprdl.ca",
                "employerId": 2,
                "enterprise": {
                    "address": "123 rue bacon",
                    "cityId": 637,
                    "email": "abc@hotmail.com",
                    "id": 2,
                    "isTemporary": false,
                    "name": "pistouille",
                    "phone": "111-222-3333"
                },
                "hoursPerWeek": 32.0,
                "id": 5,
                "isApproved": true,
                "last_modified_by_id": 2,
                "offerDebut": (() => {
                    const date = new Date();
                    date.setDate(date.getDate() + 1);
                    return date.toISOString().split('T')[0];
                })(),
                "offerLink": "https://google.ca",
                "salary": "23456789",
                "schedules": [
                    {
                        "description": "Emploi d'\u00e9t\u00e9",
                        "id": 2
                    }
                ],
                "studyPrograms": [
                    {
                        "id": 3,
                        "name": "Gestion et intervention en loisir"
                    }
                ],
                "title": "\ud83e\udd96"
            }]
        }
    },

    jobOfferUpdateInvalid: {
        url: '*/**/jobOffer/*',
        response: {
            status: 400,
            json: {
                field: "title",
                message: "Ceci est un retour pour tester les erreurs back-end pour modifier."
            }
        }
    },

    jobOfferVerifyURLWITHBADLINK: {
        url: '*/**/jobOffer/verifyURL',
        response: {
            status: 400,
            json: {
                message: "URL is not accessible"
            }
        }
    },
} satisfies Record<string, MockConfig>;


