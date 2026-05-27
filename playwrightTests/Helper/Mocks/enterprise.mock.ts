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
    },
    enterpriseEmployer: {
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
    },
    all: {
        url: '*/**/enterprise/all',
        response: {
            status: 200,
            json: [
                {
                    id: 1,
                    name: 'Entreprise Test 1',
                    email: 'test1@example.com',
                    phone: '4185551111',
                    address: '123 Rue Test',
                    cityId: 1,
                    isTemporary: false
                },
                {
                    id: 2,
                    name: 'Entreprise Test 2',
                    email: 'test2@example.com',
                    phone: '4185552222',
                    address: '456 Avenue Test',
                    cityId: 2,
                    isTemporary: false
                },
                {
                    id: 3,
                    name: 'Montreal Solutions',
                    email: 'contact@montreal.com',
                    phone: '5145553333',
                    address: '789 Blvd Montreal',
                    cityId: 3,
                    isTemporary: false
                }
            ]
        }
    },
    createNew: {
        url: '*/**/enterprise/new',
        response: {
            status: 200,
            json: {
                id: 4,
                name: 'Nouvelle Entreprise',
                email: 'nouvelle@example.com',
                phone: '4185554444',
                address: '321 Rue Nouvelle',
                cityId: 1,
                isTemporary: false
            }
        }
    },
    update: {
        url: '*/**/enterprise/1',
        response: {
            status: 200,
            json: { message: 'enterprise updated' }
        }
    }
} satisfies Record<string, MockConfig>;