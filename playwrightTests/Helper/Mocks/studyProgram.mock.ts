import { MockConfig } from "../types";
export const studyProgramMocks = {
    success: {
        url: '*/**/studyProgram/studyPrograms',
        response: {
            status: 200,
            json: [{
                "id": 9,
                "name": "Arts visuels"
            }]
        }
    },
    notFound: {
        url: '*/**/studyProgram/studyPrograms',
        response: {
            status: 404,
            json: {
                message: "Pas de programme d'études trouvé"
            }
        }
    }
} satisfies Record<string, MockConfig>;

