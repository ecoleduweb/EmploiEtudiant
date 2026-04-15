import { MockConfig } from "../types";

export const cityMocks = {
    success: {
        url: '*/**/city/all',
        response: {
            status: 200,
            json: [{
                "city": "Abercorn",
                "id": 1,
                "region": "Mont\u00e9r\u00e9gie"
            }]
        }
    },
    // this mock is add for the test 'Vérifier que la nouvelle ville a été ajoutée à la liste' in test.enterpriseManagement.spec.ts, to mock the response of the API call to get the city by id after adding a new city
    one: {
        url: '*/**/city/1', 
        response: {
            status: 200,
            json: {
                "city": "Abercorn",
                "id": 1,
                "region": "Mont\u00e9r\u00e9gie"
            }
        }
    },
    notFound: {
        url: '*/**/city/all',
        response: {
            status: 404,
            json: { message: "city not found" }
        }
    }
} satisfies Record<string, MockConfig>;