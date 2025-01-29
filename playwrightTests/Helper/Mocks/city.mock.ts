import { MockConfig } from "../types";
export const cityMocks = {
    success: {
        url: '*/**/city/all',
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
            json: {
                message: "city not found"
            }
        }
    }
} satisfies Record<string, MockConfig>;


