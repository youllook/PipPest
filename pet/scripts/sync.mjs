// 把網頁原型與素材複製進 Tauri 的前端資料夾 dist/
// 原型仍以 prototype/pip.html 為準，這裡只做搬運，不要直接改 dist/
import { cpSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..', '..');           // claudeTheme/
const dist = join(here, '..', 'dist');

rmSync(dist, { recursive: true, force: true });
mkdirSync(dist, { recursive: true });
cpSync(join(root, 'prototype', 'pip.html'), join(dist, 'index.html'));
for (const d of ['parts', 'expr', 'props', 'anim']) {
  cpSync(join(root, 'assets', d), join(dist, 'assets', d), { recursive: true });
}
console.log('synced →', dist);
