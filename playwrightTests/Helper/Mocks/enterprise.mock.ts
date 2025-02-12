import { MockConfig } from "../types";
export const enterpriseMocks = {
    notFound: {
        url: '*/**/enterprise/currentEnterprise',
        response: {
            status: 404,
            json: { message: "Enterprise not found" }
        }
    },
    success: {
        url: '*/**/enterprise/currentEnterprise',
        response: {
            status: 200,
            json: {
                "address": "test",
                "cityId": 1,
                "email": "test@gmail.com",
                "id": 7,
                "isTemporary": false,
                "name": "test",
                "phone": "1231234123"
            }
        }
    }
} satisfies Record<string, MockConfig>;