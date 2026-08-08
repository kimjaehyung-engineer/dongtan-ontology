import fs from 'fs';
import { JSDOM } from 'jsdom';

const htmlPath = 'c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/09.공정표/동탄트램_Time_Chainage_공정표_대시보드.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

console.log("=== Launching JSDOM Virtual Browser Simulation ===");

try {
  const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
  const { window } = dom;
  const { document } = window;

  // Mock getBoundingClientRect
  window.Element.prototype.getBoundingClientRect = function() {
    return {
      width: 1200,
      height: 600,
      top: 0,
      left: 0,
      bottom: 600,
      right: 1200
    };
  };

  // Trigger load
  window.dispatchEvent(new window.Event('load'));

  setTimeout(() => {
    const tree = document.getElementById('wbs-tree-container');
    const svg = document.getElementById('tc-svg');

    console.log("Tree innerHTML length:", tree ? tree.innerHTML.length : 0);
    console.log("SVG innerHTML length:", svg ? svg.innerHTML.length : 0);
    console.log("SVG child elements count:", svg ? svg.children.length : 0);

    if (!tree || tree.children.length === 0) {
      console.error("❌ FAILURE: Tree container is completely empty!");
    } else {
      console.log(`✓ SUCCESS: Tree container populated with ${tree.children.length} items.`);
    }

    if (!svg || svg.children.length === 0) {
      console.error("❌ FAILURE: SVG canvas is completely empty!");
    } else {
      console.log(`✓ SUCCESS: SVG canvas populated with ${svg.children.length} elements.`);
    }

  }, 300);

} catch (err) {
  console.error("❌ JSDOM Runtime Error:", err);
}
