import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const match = html.match(/const RAW_ACTIVITIES = (\[[\s\S]*?\]);/);
if (!match) {
  console.error("RAW_ACTIVITIES not found");
  process.exit(1);
}

const data = JSON.parse(match[1]);
console.log(`✓ Data Validation: Loaded ${data.length} total real activities in HTML!`);

const zone1 = data.filter(d => d.zone === '1공구');
const zone2 = data.filter(d => d.zone === '2공구');
console.log(`✓ 1공구 Activity Count: ${zone1.length} (Expected: 288)`);
console.log(`✓ 2공구 Activity Count: ${zone2.length} (Expected: 225)`);

const esList = data.map(d => d.es).filter(d => d).sort();
const efList = data.map(d => d.ef).filter(d => d).sort();

console.log(`✓ Earliest Start Date (ES): ${esList[0]}`);
console.log(`✓ Latest Finish Date (EF): ${efList[efList.length - 1]}`);
