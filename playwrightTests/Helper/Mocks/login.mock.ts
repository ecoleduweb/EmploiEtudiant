import { MockConfig } from "../types";


/*const generateToken = (isModerator) => {
    const payload = {
        email: "test@gmail.com",
        exp: Math.floor((Date.now() + 30 * 60 * 1000) / 1000), // 30 minutes from now
        active: true,
        isModerator: isModerator,
        firstName: "",
        lastName: ""
    };

    // Clé secrète pour les tests
    const SECRET_KEY = 'cle-secrette-pour-les-tests';

    return jwt.sign(payload, SECRET_KEY);
};*/

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
                isModerator: false,
                email: "test@gmail.com",
                firstname: "Test",
                lastname: "User",
            }
        }
    },
    successModerator: {
        url: '*/**/user/login',
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