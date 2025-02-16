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
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNzM5NzM5NDY2LCJhY3RpdmUiOnRydWUsImlzTW9kZXJhdG9yIjpmYWxzZSwiZmlyc3ROYW1lIjoiIiwibGFzdE5hbWUiOiIifQ.Fft29KxIDl3KLPrJ_vxQONS1qd4kzor_Fighq7zH3Hk"
            }
        }
    }
} satisfies Record<string, MockConfig>;