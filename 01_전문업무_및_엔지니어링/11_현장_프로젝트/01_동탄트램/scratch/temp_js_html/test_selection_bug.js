import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const actMatch = html.match(/const RAW_ACTIVITIES = (\[[\s\S]*?\]);/);
const splitMatch = html.match(/const SECTION_SPLITS = (\[[\s\S]*?\]);/);

const RAW_ACTIVITIES = JSON.parse(actMatch[1]);
const SECTION_SPLITS = JSON.parse(splitMatch[1]);

let currentZone = 'ALL';
let currentCategoryTab = 'ALL';
let selectedSplitKeys = new Set(['1공구_일반부지 1구간']);
let searchQuery = '';
let selectedSubSec = null;

function getGroupedSplits() {
  const groups = {};
  SECTION_SPLITS.forEach(item => {
    if (currentZone !== 'ALL' && item.zone !== currentZone) return;
    if (currentCategoryTab !== 'ALL' && !item.splitGroup.includes(currentCategoryTab)) return;

    const gKey = `${item.zone}_${item.splitGroup}`;
    if (selectedSplitKeys.size > 0 && !selectedSplitKeys.has(gKey)) return;

    if (!groups[gKey]) {
      groups[gKey] = {
        zone: item.zone,
        groupName: item.splitGroup,
        items: []
      };
    }
    groups[gKey].items.push(item);
  });
  return Object.values(groups).filter(g => g.items.length > 0);
}

const groups = getGroupedSplits();
console.log(`✓ Filtered Groups count for '1공구_일반부지 1구간': ${groups.length}`);

if (groups.length > 0) {
  let allStarts = [], allEnds = [];
  groups.forEach(g => {
    g.items.forEach(it => {
      allStarts.push(it.startM / 1000.0);
      allEnds.push(it.endM / 1000.0);
    });
  });
  const realMin = Math.min(...allStarts);
  const realMax = Math.max(...allEnds);
  console.log(`✓ realMin: ${realMin}, realMax: ${realMax}`);
  
  const span = Math.max(0.5, realMax - realMin);
  const minKm = Math.max(0.0, realMin - (span * 0.2));
  const maxKm = Math.min(20.5, realMax + (span * 0.2));
  
  console.log(`✓ Calculated minKm: ${minKm}, maxKm: ${maxKm}`);

  // Test SVG calculation
  const width = 1000, height = 600;
  const padL = 75, padR = 50, padT = 45, padB = 65;
  const graphW = width - padL - padR;
  const graphH = height - padT - padB;

  const getX = (km) => padL + ((km - minKm) / (maxKm - minKm)) * graphW;
  
  groups.forEach(g => {
    g.items.forEach(item => {
      const sKm = item.startM / 1000.0;
      const eKm = item.endM / 1000.0;
      console.log(`Item '${item.sectionName}': sKm=${sKm}, eKm=${eKm} -> x1=${getX(sKm)}, x2=${getX(eKm)}`);
    });
  });
}
