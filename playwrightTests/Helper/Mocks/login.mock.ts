import { MockConfig } from "../types";
export const loginMocks = {
    notFound: {
        url: '*/**/user/login',
        response: {
            status: 404,
            json: { message: "User not found" }
        }
    },
    success: {
        url: '*/**/user/login',
        response: {
            status: 200,
            json: {
                "email": "test@gmail.com",
                "exp": 1739397843,
                "active": true,
                "isModerator": false,
                "firstName": "test",
                "lastName": "test"
            }
        }
    }
} satisfies Record<string, MockConfig>;