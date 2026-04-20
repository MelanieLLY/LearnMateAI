import { test, expect } from '@playwright/test';

test('Student Flow: login and browse modules', async ({ page }) => {
  // 自动打开首页
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('欢迎使用 LearnMateAI');

  // 点击登录
  await page.getByRole('link', { name: /登录/ }).click();
  await expect(page.getByRole('heading', { name: '登录' })).toBeVisible();

  // 填入学生凭据并登录
  await page.locator('input[type="email"]').fill('alex.johnson@student.edu');
  await page.locator('input[type="password"]').fill('dUfkhVsX8vJQ');
  await page.getByRole('button', { name: /登录/ }).click();

  // 登录成功后自动跳转到学生 Dashboard (/student)
  await expect(page).toHaveURL(/\/student/);
  await expect(page.locator('h1')).toContainText('学生端：模块浏览与学习');
  await expect(page.getByText('alex.johnson@student.edu')).toBeVisible();

  // 验证大模块呈现 (选课大厅 / 我的学习模块)
  await expect(page.getByRole('heading', { name: /选课大厅/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /我的学习模块/ })).toBeVisible();
});

