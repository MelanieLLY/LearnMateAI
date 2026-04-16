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
  await page.locator('input[type="password"]').fill('A9TQ6zQgyH3O');
  await page.getByRole('button', { name: /登录/ }).click();

  // 验证登录成功，跳转回主页
  await expect(page.locator('h1')).toContainText('欢迎使用 LearnMateAI');
  await expect(page.getByText('alex.johnson@student.edu')).toBeVisible();
  
  // 浏览模块列表 (进入学生 Dashboard)
  await page.getByRole('link', { name: /学生 Dashboard/ }).click();
  await expect(page.getByRole('heading', { name: /学生端：模块浏览与学习/ })).toBeVisible();

  // 验证大模块呈现 (选课大厅 / 我的学习模块)
  await expect(page.getByRole('heading', { name: /选课大厅/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /我的学习模块/ })).toBeVisible();
});
