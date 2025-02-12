import { MockConfig } from "../types";
export const jobOfferMocks = {
    jobOfferNew: {
        url: '*/**/jobOffer/new',
        response: {
            status: 200,
            json: { "message": "Offre créée" }
        }
    },
    jobOfferEmployer: {
        url: '*/**/jobOffer/employer/*',
        response: {
            status: 404,
            json: { "message": "Offres non trouvées" }
        }
    },
    jobOfferVerifyURL: {
        url: '*/**/jobOffer/verifyURL',
        response: {
            status: 200,
            json: {
                message: "URL is accessible"
            }
        }
    }
} satisfies Record<string, MockConfig>;


