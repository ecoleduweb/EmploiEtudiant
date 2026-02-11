import { MockConfig } from "../types";

export const userMocks = {
    meUnauthorized: {
        url: '*/**/user/me',
        response: {
            status: 404,
            json: { message: "Token is invalid or expired" }
        }
    },
    meUser: {
        url: '*/**/user/me',
        response: {
            status: 200,
            json: {
                isModerator: false,
                email: "test@gmail.com",
                firstname: "Test",
                lastname: "User",
            }
        }
    },
    meModerator: {
        url: '*/**/user/me',
        response: {
            status: 200,
            json: {
                isModerator: true,
                email: "test@gmail.com",
                firstname: "Test",
                lastname: "Admin",
            }
        }
    }
} satisfies Record<string, MockConfig>;