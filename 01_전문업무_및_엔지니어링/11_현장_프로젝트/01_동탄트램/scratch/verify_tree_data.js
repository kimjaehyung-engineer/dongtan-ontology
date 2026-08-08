import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const matchAct = html.match(/const RAW_ACTIVITIES = (\[[\s\S]*?\]);/);
const matchSplit = html.match(/const SECTION_SPLITS = (\[[\s\S]*?\]);/);

if (!matchAct || !matchSplit) {
  console.error("Data missing in HTML");
  process.exit(1);
}

const acts = JSON.parse(matchAct[1]);
const splits = JSON.parse(matchSplit[1]);

console.log(`✓ Data Validation: Loaded ${acts.length} real activities (Expected: 513)`);
console.log(`✓ Data Validation: Loaded ${splits.length} section splits (Expected: 123)`);

const groupNames = Array.from(new Set(splits.map(s => `${s.zone}_${s.splitGroup}`)));
console.log(`✓ Unique Section Split Groups: ${groupNames.length} groups`);
console.log("Sample Groups:", groupNames.slice(0, 8));
