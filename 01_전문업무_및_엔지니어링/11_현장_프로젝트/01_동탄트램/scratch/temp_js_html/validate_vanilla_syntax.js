import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error("No <script> tag found!");
  process.exit(1);
}

try {
  new Function(scriptMatch[1]);
  console.log("SUCCESS: Pure Vanilla JS script syntax is 100% PERFECT and Error-Free!");
} catch (e) {
  console.error("Syntax Error in script:", e);
}
