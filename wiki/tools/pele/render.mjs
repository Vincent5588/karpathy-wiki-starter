#!/usr/bin/env node
// 規則 W 的 Pele 渲染器：把 Mermaid 原文畫成帶深色樣式的獨立 SVG，可另出 PNG、HTML。
//
// 用法：
//   node render.mjs <輸入.mmd 或 .md> <輸出.svg> [--png 輸出.png] [--html 輸出.html] [--index N]
//   .md 檔取第 N 個 ```mermaid 區塊（從 1 數，預設 1）。
//
// Pele 裝在本機、不放進 vault：macOS／Linux 預設 ~/.local/share/pele-render，
// Windows 預設 %LOCALAPPDATA%\pele-render；可用環境變數 PELE_RENDER_HOME 改。
// 沒裝或版本不對就停下，並印出安裝指令（install.sh／install.ps1）。
//
// 配色只來自同資料夾的 rule-w-pele.css（唯一一份），原樣嵌進 SVG，所以 SVG 單獨打開也是深色。

import { existsSync, readFileSync, renameSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { homedir, tmpdir } from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const FONT = 'Arial, PingFang TC, Microsoft JhengHei, sans-serif';

function installDir() {
  if (process.env.PELE_RENDER_HOME) return process.env.PELE_RENDER_HOME;
  if (process.platform === 'win32') return join(process.env.LOCALAPPDATA || join(homedir(), 'AppData', 'Local'), 'pele-render');
  return join(homedir(), '.local', 'share', 'pele-render');
}

function fail(msg, code = 1) {
  console.error(`[pele-render] ${msg}`);
  process.exit(code);
}

function installHint() {
  return process.platform === 'win32'
    ? `powershell -ExecutionPolicy Bypass -File "${join(HERE, 'install.ps1')}"`
    : `sh "${join(HERE, 'install.sh')}"`;
}

// 先寫同目錄暫存檔再改名（CLAUDE.md §13 鐵則 4：失敗時不留半個檔）
function writeAtomic(path, text) {
  const tmp = `${path}.tmp-${process.pid}`;
  writeFileSync(tmp, text, { encoding: 'utf-8' });
  renameSync(tmp, path);
}

function parseArgs(argv) {
  const pos = [];
  const opt = { index: 1 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--png' || a === '--html' || a === '--index') {
      if (i + 1 >= argv.length) fail(`${a} 後面要接值`);
      opt[a.slice(2)] = argv[++i];
    } else pos.push(a);
  }
  if (pos.length !== 2) fail('用法：node render.mjs <輸入.mmd|.md> <輸出.svg> [--png 輸出.png] [--html 輸出.html] [--index N]');
  opt.index = Number(opt.index);
  if (!Number.isInteger(opt.index) || opt.index < 1) fail('--index 要是 1 以上的整數');
  return { input: resolve(pos[0]), output: resolve(pos[1]), ...opt };
}

function readSource(input, index) {
  const text = readFileSync(input, { encoding: 'utf-8' }).replace(/\r\n/g, '\n');
  if (!input.toLowerCase().endsWith('.md')) return text;
  const blocks = [...text.matchAll(/^```mermaid[^\n]*\n([\s\S]*?)^```/gm)].map(m => m[1]);
  if (blocks.length < index) fail(`${input} 只有 ${blocks.length} 個 mermaid 區塊，沒有第 ${index} 個`);
  return blocks[index - 1];
}

async function loadPele() {
  const want = JSON.parse(readFileSync(join(HERE, 'package.json'), { encoding: 'utf-8' })).dependencies.pele;
  const pkg = join(installDir(), 'node_modules', 'pele', 'package.json');
  if (!existsSync(pkg)) fail(`本機還沒裝 Pele（找不到 ${pkg}）。安裝：${installHint()}`, 2);
  const have = JSON.parse(readFileSync(pkg, { encoding: 'utf-8' })).version;
  if (have !== want) fail(`本機 Pele 是 ${have}，vault 鎖定 ${want}。重裝：${installHint()}`, 3);
  return import(pathToFileURL(join(installDir(), 'node_modules', 'pele', 'dist', 'pele.js')).href);
}

function findBrowser() {
  const c = process.platform === 'darwin'
    ? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
    : process.platform === 'win32'
      ? ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe']
      : ['/usr/bin/google-chrome', '/usr/bin/chromium'];
  return c.find(p => existsSync(p));
}

function page(svg) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;padding:24px;background:#181818}</style></head><body>${svg}</body></html>\n`;
}

const args = parseArgs(process.argv.slice(2));
const source = readSource(args.input, args.index);
const css = readFileSync(join(HERE, 'rule-w-pele.css'), { encoding: 'utf-8' });
const { render } = await loadPele();

let result;
try {
  result = render(source, { idPrefix: 'rw', fontFamily: FONT });
} catch (e) {
  fail(`Pele 畫不出來：${e.message}。這張圖改用原生 Mermaid（規則 W §W.8）`, 4);
}
const svg = result.svg.replace(/(<svg\b[^>]*>)/, `$1<style>${css}</style>`);
writeAtomic(args.output, svg);
console.log(`SVG  ${args.output}（${Math.round(result.width)}×${Math.round(result.height)}）`);

if (args.html) {
  writeAtomic(resolve(args.html), page(svg));
  console.log(`HTML ${resolve(args.html)}`);
}

if (args.png) {
  const browser = findBrowser();
  if (!browser) fail('找不到 Chrome 或 Edge，PNG 沒有產出（SVG 已完成）', 5);
  const dir = mkdtempSync(join(tmpdir(), 'pele-render-'));
  try {
    const html = join(dir, 'page.html');
    writeFileSync(html, page(svg), { encoding: 'utf-8' });
    const w = Math.ceil(result.width) + 48;
    const h = Math.ceil(result.height) + 48;
    const png = resolve(args.png);
    execFileSync(browser, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
      `--window-size=${w},${h}`, `--screenshot=${png}`, pathToFileURL(html).href], { stdio: 'ignore' });
    if (!existsSync(png)) fail('瀏覽器沒有寫出 PNG', 5);
    console.log(`PNG  ${png}`);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}
