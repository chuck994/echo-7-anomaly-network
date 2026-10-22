import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#case-count')).not.toHaveText('—');
  await expect(page.locator('#case-count')).not.toHaveText('0');
  // The archive results live inside #pageview, which is intentionally hidden on the desk.
  // Assert the records were rendered without requiring a hidden element to be visible.
  await expect(page.locator('#results .record').first()).toHaveCount(1);
});

test('all twelve desk notes open their matching archive view', async ({ page }) => {
  const notes = page.locator('#homeview [data-page]');
  await expect(notes).toHaveCount(13); // 12 board notes plus the desk's featured shortcut
  for (const note of await page.locator('#homeview .note[data-page]').all()) {
    const id = await note.getAttribute('data-page');
    await note.click();
    await expect(page.locator('#pageview')).toHaveClass(/active/);
    await expect(page.locator('#pagetitle')).not.toBeEmpty();
    await expect(page).toHaveURL(new RegExp('#' + id + '$'));
    await page.locator('#back-home').click();
    await expect(page.locator('#homeview')).not.toHaveClass(/hidden/);
  }
});

test('search narrows results and clear search restores them', async ({ page }) => {
  await page.locator('[data-page="database"]').click();
  const initial = await page.locator('#results .record').count();
  await page.locator('#search').fill('GIMBAL');
  await expect(page.locator('#results')).toContainText(/GIMBAL/i);
  expect(await page.locator('#results .record').count()).toBeLessThan(initial);
  await page.locator('#search').fill('');
  await expect(page.locator('#results .record').first()).toBeVisible();
});

test('type and year filters are populated and can be applied', async ({ page }) => {
  await page.locator('[data-page="research"]').click();
  expect(await page.locator('#kind-filter option').count()).toBeGreaterThan(1);
  expect(await page.locator('#year-filter option').count()).toBeGreaterThan(1);
  await page.locator('#kind-filter').selectOption({ index: 1 });
  await expect(page.locator('#results .record').first()).toBeVisible();
  const selectedKind = await page.locator('#kind-filter').inputValue();
  await expect(page.locator('#results .record .tag').first()).toContainText(selectedKind.replace(/-/g, ' '));
});

test('browser back returns to the desk and layout has no horizontal overflow on mobile', async ({ page }) => {
  await page.locator('[data-page="timeline"]').click();
  await page.goBack();
  await expect(page.locator('#homeview')).not.toHaveClass(/hidden/);
  await page.setViewportSize({ width: 390, height: 844 });
  const dimensions = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth + 1);
});

test('source shelf renders links with safe new-tab attributes', async ({ page }) => {
  await page.locator('[data-page="sources"]').click();
  const link = page.locator('#results a.source-link').first();
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute('target', '_blank');
  await expect(link).toHaveAttribute('rel', /noopener/);
});
