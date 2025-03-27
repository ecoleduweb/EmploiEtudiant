import { MockConfig } from "../types";
export const employementScheduleByOfferIdMocks = {
    success: {
        url: '*/**/employmentSchedule/getByOfferId/*',
        response: {
            status: 200,
            json: [{
                "description": "Temps plein",
                "id": 1
            }]
        }
    }
} satisfies Record<string, MockConfig>;