import { MockConfig } from "../types";

export const userMocks = {
    meUnauthorized: {
        url: '*/**/user/me',
        response: {
            status: 401,
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
    },
    all: {
        url: '*/**/user/all',
        response: {
            status: 200,
            json: {
                users: [
                    { id: 10, firstName: "Jean", lastName: "Employé", email: "jean@test.com" },
                    { id: 11, firstName: "Marc", lastName: "Admin", email: "marc@test.com" }
                ]
            }
        }
    }
} satisfies Record<string, MockConfig>;