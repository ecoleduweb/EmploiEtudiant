import { MockConfig } from "../types";

export const userMocks = {
    meUnauthorized: {
        url: '*/**/auth/me',
        response: {
            status: 401,
            json: { message: "Token is invalid or expired" }
        }
    },
    meUser: {
        url: '*/**/auth/me',
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
        url: '*/**/auth/me',
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