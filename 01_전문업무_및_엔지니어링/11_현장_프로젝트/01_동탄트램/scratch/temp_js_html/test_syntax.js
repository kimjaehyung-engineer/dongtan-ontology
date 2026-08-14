import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const scriptMatch = html.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error("No script match");
  process.exit(1);
}

const jsCode = scriptMatch[1];
const lines = jsCode.split('\n');
console.log(`Total lines in script: ${lines.length}`);

// Check for unclosed braces or parenthesis
let openBrace = 0, closeBrace = 0;
let openParen = 0, closeParen = 0;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  openBrace += (line.match(/\{/g) || []).length;
  closeBrace += (line.match(/\}/g) || []).length;
  openParen += (line.match(/\(/g) || []).length;
  closeParen += (line.match(/\)/g) || []).length;
}

console.log(`Braces: { = ${openBrace}, } = ${closeBrace}, Match: ${openBrace === closeBrace}`);
console.log(`Parens: ( = ${openParen}, ) = ${closeParen}, Match: ${openParen === closeParen}`);

// Search for any unhandled import statements
const unhandledImports = lines.filter(l => l.trim().startsWith('import '));
console.log(`Unhandled import statements: ${unhandledImports.length}`);
if (unhandledImports.length > 0) {
  console.log("Imports found:", unhandledImports);
}
