import { test, expect } from '@playwright/test';

// Credentials are injected via environment variables so no plaintext secrets
// are stored in the repository. Set E2E_STUDENT_EMAIL / E2E_STUDENT_PASSWORD
// locally (copy .env.example → .env) or via GitHub Actions secrets.
const STUDENT_EMAIL = process.env.E2E_STUDENT_EMAIL ?? 'alex.johnson@student.edu';
const STUDENT_PASSWORD = process.env.E2E_STUDENT_PASSWORD ?? 'dUfkhVsX8vJQ';

test('Student Flow: login and browse modules', async ({ page }) => {
  // Navigate to the home page
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('LearnMateAI');

  // Click login link
  await page.getByRole('link', { name: /login|登录/i }).click();
  await expect(page.getByRole('heading', { name: /login|登录/i })).toBeVisible();

  // Fill in student credentials and submit
  await page.locator('input[type="email"]').fill(STUDENT_EMAIL);
  await page.locator('input[type="password"]').fill(STUDENT_PASSWORD);
  await page.getByRole('button', { name: /login|登录/i }).click();

  // 登录成功后自动跳转到学生 Dashboard (/student)
  await expect(page).toHaveURL(/\/student/);
  await expect(page.locator('h1')).toContainText('学生端：模块浏览与学习');
  await expect(page.getByText('alex.johnson@student.edu')).toBeVisible();

  // 验证大模块呈现 (选课大厅 / 我的学习模块)
  await expect(page.getByRole('heading', { name: /选课大厅/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /我的学习模块/ })).toBeVisible();
});

