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
    },
    all: {
        url: '*/**/user/all',
        response: {
            status: 200,
            json: [
                {
                    id: 1,
                    firstName: 'John1',
                    lastName: 'Doe1',
                    email: 'John1@gmail.com',
                    active: true,
                    isModerator: false,
                    verified: false,
                    enterpriseId: 1
                },
                {
                    id: 2,
                    firstName: 'John2',
                    lastName: 'Doe2',
                    email: 'John2@gmail.com',
                    active: true,
                    isModerator: false,
                    verified: false,
                    enterpriseId: 1
                },
                {
                    id: 3,
                    firstName: 'John3',
                    lastName: 'Doe3',
                    email: 'John3@gmail.com',
                    active: true,
                    isModerator: false,
                    verified: false,
                    enterpriseId: 1
                },
            ]
        }
    }
} satisfies Record<string, MockConfig>;