import { LAST_MONTH, NEXT_MONTH, NOW } from "../../tests/fixtures";
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
      json: [
        {
          "address": "123 rue bacon",
          "approbationMessage": "\ud83e\udd96",
          "lastModifiedDate": NEXT_MONTH.toISOString().split('T')[0],
          "approvedDate": NEXT_MONTH.toISOString().split('T')[0],
          "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
          "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
          "description": "\ud83e\udd96",
          "email": "bob@cegeprdl.ca",
          "userId": 2,
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
          "offerDebut": '2024-02-26',
          "offerLink": "https://google.ca",
          "salary": "23456789",
          "employmentSchedules": [
            {
              "description": "Emploi d'été",
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
            "address": "maison",
            "approbationMessage": "sdsd",
            "lastModifiedDate": NEXT_MONTH.toISOString().split('T')[0],
            "approvedDate": NEXT_MONTH.toISOString().split('T')[0],
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": LAST_MONTH.toISOString().split('T')[0],
            "description": "Lorem ipsum dolor sit amet",
            "email": "vincent.bouch1@gmail.com",
            "userId": 2,
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
            "offerDebut": NOW.toISOString().split('T')[0],
            "offerLink": "https://nodejs.org/fr/blog/release/v20.11.1",
            "salary": "10",
            "employmentSchedules": [{ "description": "Emploi d'été", "id": 2 }],
            "studyPrograms": [{ "id": 1, "name": "Design d'intérieur" }],
            "title": "expirée"
          },
          {
            "address": "sda",
            "approbationMessage": "",
            "approvedDate": null,
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
            "description": "Lorem ipsum dolor sit amet",
            "email": "asdasd@asdasd.ca",
            "userId": 2,
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
            "offerDebut": NOW.toISOString().split('T')[0],
            "offerLink": "https://youtu.be",
            "salary": "44",
            "employmentSchedules": [{ "description": "Emploi d'été", "id": 2 }],
            "studyPrograms": [{ "id": 1, "name": "Design d'intérieur" }],
            "title": "REFUSÉ"
          },
          {
            "address": "80 rue frontenac",
            "approbationMessage": null,
            "approvedDate": NEXT_MONTH.toISOString().split('T')[0],
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
            "description": "Merci !",
            "email": "courriel@contact.com",
            "userId": 6,
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
            "offerDebut": NEXT_MONTH.toISOString().split('T')[0],
            "offerLink": "",
            "salary": "66",
            "employmentSchedules": [{ "description": "Temps partiel", "id": 3 }],
            "studyPrograms": [{ "id": 2, "name": "Éducation à l'enfance" }],
            "title": "toBeAnnounced"
          },
          {
            "address": "80 rue frontenac",
            "approbationMessage": null,
            "approvedDate": NEXT_MONTH.toISOString().split('T')[0],
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
            "description": "Merci !",
            "email": "courriel@contact.com",
            "userId": 6,
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
            "offerDebut": NOW.toISOString().split('T')[0],
            "offerLink": "",
            "salary": "66",
            "employmentSchedules": [{ "description": "Temps partiel", "id": 3 }],
            "studyPrograms": [{ "id": 2, "name": "Éducation à l'enfance" }],
            "title": "toBeApprovedPourVrai"
          },
          {
            "address": "80 rue frontenac",
            "approbationMessage": null,
            "approvedDate": null,
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
            "description": "dxfchkl",
            "email": "ll@cegeprdl.ca",
            "userId": 5,
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
            "offerDebut": NOW.toISOString().split('T')[0],
            "offerLink": "",
            "salary": "77",
            "employmentSchedules": [{ "description": "Temps partiel", "id": 3 }],
            "studyPrograms": [{ "id": 2, "name": "Éducation à l'enfance" }],
            "title": "En attente de l'approbation"
          },
          {
            "address": "quelque part",
            "approbationMessage": "Refusée par l’administrateur",
            "approvedDate": null,
            "dateEntryOffice": NEXT_MONTH.toISOString().split('T')[0],
            "deadlineApply": NEXT_MONTH.toISOString().split('T')[0],
            "description": "Offre explicitement refusée",
            "email": "refuse@exemple.com",
            "userId": 9,
            "enterprise": {
              "address": "qwe#",
              "cityId": 637,
              "email": "qwe@dsd.ca",
              "id": 2,
              "isTemporary": false,
              "name": "sqd",
              "phone": "1231238888"
            },
            "hoursPerWeek": 10.0,
            "id": 105,
            "isApproved": false,
            "last_modified_by_id": 3,
            "offerDebut": NOW.toISOString().split('T')[0],
            "offerLink": "",
            "salary": "20",
            "employmentSchedules": [
              { "description": "Temps partiel", "id": 3 }
            ],
            "studyPrograms": [
              { "id": 2, "name": "Éducation à l'enfance" }
            ],
            "title": "offreRefusee"
          }
        ]
    }
  }
} satisfies Record<string, MockConfig>;
