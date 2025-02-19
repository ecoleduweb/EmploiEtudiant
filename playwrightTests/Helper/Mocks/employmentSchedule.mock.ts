import { MockConfig } from "../types";
export const employmentScheduleMocks = {
    success: {
        url: '*/**/employmentSchedule/all',
        response: {
            status: 200,
            json: [{
                "description": "Temps plein",
                "id": 1
            }]
        }
    },
    notFound: {
        url: '*/**/employmentSchedule/all',
        response: {
            status: 404,
            json: [{
                message: "pas d'horaire de travail trouvé"
            }]
        }
    }
} satisfies Record<string, MockConfig>;
