import { test as base, expect } from '@playwright/test';


 const FIXED_LOCAL_ISO = '2024-02-25T12:00:00-05:00';
 const FIXED_NOW = new Date(FIXED_LOCAL_ISO);

export const test = base.extend({
  page: async ({ page }, use) => {
    await page.clock.install({ time: FIXED_NOW });
    await use(page);
  },
});

export { expect };
