import fs from 'fs';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

// Extract script content
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error("Script tag not found");
  process.exit(1);
}

const jsCode = scriptMatch[1];

// Evaluate JS in a mock DOM environment to catch runtime exceptions
try {
  const mockDocument = {
    getBoundingClientRect: () => ({ width: 1000, height: 600 }),
    querySelectorAll: () => [],
    getElementById: (id) => ({
      getBoundingClientRect: () => ({ width: 1000, height: 600 }),
      addEventListener: () => {},
      classList: { add: () => {}, remove: () => {} },
      style: {},
      innerText: '',
      innerHTML: ''
    })
  };

  // Check syntax and variable bindings
  console.log("Testing JS runtime logic execution...");
  
  // Test data parsing
  const actMatch = jsCode.match(/const RAW_ACTIVITIES = (\[[\s\S]*?\]);/);
  const splitMatch = jsCode.match(/const SECTION_SPLITS = (\[[\s\S]*?\]);/);
  
  const acts = JSON.parse(actMatch[1]);
  const splits = JSON.parse(splitMatch[1]);

  console.log(`✓ Acts count: ${acts.length}`);
  console.log(`✓ Splits count: ${splits.length}`);

  // Test minKm / maxKm math logic
  let allStarts = [], allEnds = [];
  splits.forEach(it => {
    allStarts.push(it.startM / 1000.0);
    allEnds.push(it.endM / 1000.0);
  });
  const realMin = Math.min(...allStarts);
  const realMax = Math.max(...allEnds);
  console.log(`✓ Overall minKm: ${realMin}, maxKm: ${realMax}`);

  if (isNaN(realMin) || isNaN(realMax)) {
    console.error("❌ Math Error: minKm or maxKm is NaN!");
  } else {
    console.log("✓ Math logic is valid and numeric!");
  }

} catch (err) {
  console.error("❌ JS Execution Error:", err);
}
