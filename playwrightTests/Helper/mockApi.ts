import { Page } from '@playwright/test';
import { MockConfig } from './types';

export class ApiMocker {
    constructor(private page: Page) { }

    async mockRoute(config: MockConfig) {
        await this.page.route(config.url, async route => {
            await route.fulfill({
                status: config.response.status,
                json: config.response.json,
                headers: config.response.headers
            });
        });
    }

    async mockRoutes(configs: MockConfig[]) {
        for (const config of configs) {
            await this.mockRoute(config);
        }
    }
}
