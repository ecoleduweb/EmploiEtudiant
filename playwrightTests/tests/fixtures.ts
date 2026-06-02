import { test as base, expect } from '@playwright/test';


const NOW = new Date('2024-02-25T12:00:00-05:00');
const NEXT_MONTH = new Date('2024-03-25T12:00:00-05:00');
const LAST_MONTH = new Date('2024-01-25T12:00:00-05:00');
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.clock.install({ time: NOW });
    await use(page);
  },
});

export { expect, NOW, NEXT_MONTH, LAST_MONTH };
