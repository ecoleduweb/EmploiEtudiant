import { MockConfig } from "../types";
export const employerMocks = {
  notFound: {
    url: '*/**/employer/currentEmployer',
    response: {
      status: 404,
      json: { message: "employer not found" }
    }
  },
  success: {
    url: '*/**/employer/currentEmployer',
    response: {
      status: 200,
      json: {
        id: 1,
        name: "Test Company",
        address: "123 Test Street"
      }
    }
  }
} satisfies Record<string, MockConfig>;