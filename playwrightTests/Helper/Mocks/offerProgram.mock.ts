import { MockConfig } from "../types";
export const offerProgramMocks = {
    success: {
        url: '*/**/offerProgram/*',
        response: {
            status: 200,
            json: [3]
        }
    }
} satisfies Record<string, MockConfig>;