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
    hasCurrentEnterprise: {
        url: '*/**/enterprise/currentEnterprise',
        response: {
            status: 200,
            json: {
                "address": "test",
                "cityId": 1,
                "email": "test@gmail.com",
                "id": 7,
                "isTemporary": false,
                "name": "employer enterprise",
                "phone": "1231234123"
            }
        }
    },
    hasTemporaryCurrentEnterprise: {
        url: '*/**/enterprise/currentEnterprise',
        response: {
            status: 200,
            json: {
                "address": "test",
                "cityId": 1,
                "email": "test@gmail.com",
                "id": 7,
                "isTemporary": true,
                "name": "temporary enterprise",
                "phone": "1231234123"
            }
        }
    },
    notFoundEmployerEnterprise: {
        url: '*/**/enterprise/currentEnterprise',
        response: {
            status: 404,
            json: {
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
                    city: {
                        id: 1,
                        city: 'Abercorn'
                    },
                    isTemporary: false,
                    users: [
                        {
                            id: 1,
                            firstName: 'John',
                            lastName: 'Doe',
                            email: 'John@gmail.com',
                            active: true,
                            isModerator: false,
                            verified: false,
                            enterpriseId: 1
                        }
                    ]
                },
                {
                    id: 2,
                    name: 'Entreprise Test 2',
                    email: 'test2@example.com',
                    phone: '4185552222',
                    address: '456 Avenue Test',
                    cityId: 2,
                    city: {
                        id: 2,
                        city: 'Montreal'
                    },
                    users: [
                        {
                            id: 2,
                            firstName: 'John2',
                            lastName: 'Doe2',
                            email: 'John@gmail.com',
                            active: true,
                            isModerator: false,
                            verified: false,
                            enterpriseId: 1
                        }
                    ],
                    isTemporary: false
                },
                {
                    id: 3,
                    name: 'Montreal Solutions',
                    email: 'contact@montreal.com',
                    phone: '5145553333',
                    address: '789 Blvd Montreal',
                    cityId: 3,
                    city: {
                        id: 3,
                        city: 'Montreal'
                    },
                    isTemporary: false,
                    users: [
                        {
                            id: 3,
                            firstName: 'John3',
                            lastName: 'Doe3',
                            email: 'John3@gmail.com',
                            active: true,
                            isModerator: false,
                            verified: false,
                            enterpriseId: 1
                        }
                    ]
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
                city: {
                    id: 1,
                    city: 'Abercorn'
                },
                isTemporary: false
            }
        }
    },
    update: {
        url: '*/**/enterprise/1',
        response: {
            status: 200,
            json: {
                id: 1,
                name: 'Mise à jour Entreprise',
                email: 'miks@ajour.com',
                phone: '123 updated',
                address: '321 Rue à jour',
                cityId: 2,
                city: {
                    id: 2,
                    city: 'Moncton'
                },
                isTemporary: false
            }
        }
    }
} satisfies Record<string, MockConfig>;