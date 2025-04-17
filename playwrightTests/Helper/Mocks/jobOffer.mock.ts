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

    jobOfferEmployerAll: {
        url: '*/**/jobOffer/employer/all?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true',
        response: {
            status: 200,
            json:
                [
                    {
                        "active": true,
                        "address": "maison",
                        "approbationMessage": "sdsd",
                        "approvedDate": "Wed, 19 Feb 2025 11:40:35 GMT",
                        "dateEntryOffice": "2025-01-29",
                        "deadlineApply": "2025-01-30",
                        "description": "Lorem ipsum dolor sit amet",
                        "email": "vincent.bouch1@gmail.com",
                        "employerId": 2,
                        "enterprise": {
                            "address": "qwe#",
                            "cityId": 637,
                            "email": "qwe@dsd.ca",
                            "id": 2,
                            "isTemporary": false,
                            "name": "sqd",
                            "phone": "1231238888"
                        },
                        "hoursPerWeek": 100.0,
                        "id": 3,
                        "isApproved": true,
                        "last_modified_by_id": 2,
                        "offerDebut": "2025-01-28",
                        "offerLink": "https://nodejs.org/fr/blog/release/v20.11.1",
                        "salary": "10",
                        "schedules": [
                            {
                                "description": "Emploi d'\u00e9t\u00e9",
                                "id": 2
                            }
                        ],
                        "studyPrograms": [
                            {
                                "id": 1,
                                "name": "Design d'int\u00e9rieur"
                            }
                        ],
                        "title": "stagiaire"
                    },
                    {
                        "active": true,
                        "address": "sda",
                        "approbationMessage": "",
                        "approvedDate": "Wed, 26 Feb 2025 11:46:55 GMT",
                        "dateEntryOffice": "2025-02-05",
                        "deadlineApply": "2025-02-05",
                        "description": "Lorem ipsum dolor sit amet",
                        "email": "asdasd@asdasd.ca",
                        "employerId": 2,
                        "enterprise": {
                            "address": "qwe#",
                            "cityId": 637,
                            "email": "qwe@dsd.ca",
                            "id": 2,
                            "isTemporary": false,
                            "name": "sqd",
                            "phone": "1231238888"
                        },
                        "hoursPerWeek": 55.0,
                        "id": 4,
                        "isApproved": false,
                        "last_modified_by_id": 2,
                        "offerDebut": "2025-02-05",
                        "offerLink": "https://youtu.be",
                        "salary": "44",
                        "schedules": [
                            {
                                "description": "Emploi d'\u00e9t\u00e9",
                                "id": 2
                            }
                        ],
                        "studyPrograms": [
                            {
                                "id": 1,
                                "name": "Design d'int\u00e9rieur"
                            }
                        ],
                        "title": "skidi"
                    },
                    {
                        "active": true,
                        "address": "80 rue frontenac",
                        "approbationMessage": null,
                        "approvedDate": null,
                        "dateEntryOffice": "2025-03-12",
                        "deadlineApply": "2028-09-25",
                        "description": "Merci !",
                        "email": "courriel@contact.com",
                        "employerId": 6,
                        "enterprise": {
                            "address": "qwe#",
                            "cityId": 637,
                            "email": "qwe@dsd.ca",
                            "id": 2,
                            "isTemporary": false,
                            "name": "sqd",
                            "phone": "1231238888"
                        },
                        "hoursPerWeek": 1.0,
                        "id": 8,
                        "isApproved": true,
                        "last_modified_by_id": 3,
                        "offerDebut": "2028-06-14",
                        "offerLink": "",
                        "salary": "66",
                        "schedules": [
                            {
                                "description": "Temps partiel",
                                "id": 3
                            }
                        ],
                        "studyPrograms": [
                            {
                                "id": 2,
                                "name": "\u00c9ducation \u00e0 l'enfance"
                            }
                        ],
                        "title": "toBeAnnounced"
                    },
                    {
                        "active": true,
                        "address": "80 rue frontenac",
                        "approbationMessage": null,
                        "approvedDate": null,
                        "dateEntryOffice": "2025-03-12",
                        "deadlineApply": "2028-09-24",
                        "description": "Merci !",
                        "email": "courriel@contact.com",
                        "employerId": 6,
                        "enterprise": {
                            "address": "qwe#",
                            "cityId": 637,
                            "email": "qwe@dsd.ca",
                            "id": 2,
                            "isTemporary": false,
                            "name": "sqd",
                            "phone": "1231238888"
                        },
                        "hoursPerWeek": 1.0,
                        "id": 8,
                        "isApproved": true,
                        "last_modified_by_id": 3,
                        "offerDebut": "2024-06-13",
                        "offerLink": "",
                        "salary": "66",
                        "schedules": [
                            {
                                "description": "Temps partiel",
                                "id": 3
                            }
                        ],
                        "studyPrograms": [
                            {
                                "id": 2,
                                "name": "\u00c9ducation \u00e0 l'enfance"
                            }
                        ],
                        "title": "toBeApprovedPourVrai"
                    },
                    {
                        "active": true,
                        "address": "80 rue frontenac",
                        "approbationMessage": null,
                        "approvedDate": null,
                        "dateEntryOffice": "2025-03-01",
                        "deadlineApply": "2025-03-15",
                        "description": "dxfchkl",
                        "email": "ll@cegeprdl.ca",
                        "employerId": 5,
                        "enterprise": {
                            "address": "qwe#",
                            "cityId": 637,
                            "email": "qwe@dsd.ca",
                            "id": 2,
                            "isTemporary": false,
                            "name": "sqd",
                            "phone": "1231238888"
                        },
                        "hoursPerWeek": 77.0,
                        "id": 7,
                        "isApproved": null,
                        "last_modified_by_id": 3,
                        "offerDebut": "2025-03-01",
                        "offerLink": "",
                        "salary": "77",
                        "schedules": [
                            {
                                "description": "Temps partiel",
                                "id": 3
                            }
                        ],
                        "studyPrograms": [
                            {
                                "id": 2,
                                "name": "\u00c9ducation \u00e0 l'enfance"
                            }
                        ],
                        "title": "papapapapa"
                    }
                ]
        }
    },
} satisfies Record<string, MockConfig>;


