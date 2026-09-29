const fs = require('fs');

const js = fs.readFileSync('scratch/script_0.js', 'utf-8');

class MockElement {
  constructor(tag, id = '') {
    this.tag = tag;
    this.id = id;
    this.children = [];
    this.style = {};
    this.classList = {
      add: (c) => this.classes.push(c),
      remove: (c) => this.classes = this.classes.filter(x => x !== c),
      toggle: (c, v) => {}
    };
    this.classes = [];
    this.innerHTML = '';
    this.innerText = '';
  }
  appendChild(child) {
    this.children.push(child);
  }
  querySelector(sel) {
    return new MockElement('div');
  }
  querySelectorAll(sel) {
    return [];
  }
}

const docElements = {
  'rootFolderPathDisplay': new MockElement('div', 'rootFolderPathDisplay'),
  'docCountBadge': new MockElement('span', 'docCountBadge'),
  'docList': new MockElement('div', 'docList')
};

global.document = {
  getElementById: (id) => docElements[id] || new MockElement('div', id),
  createElement: (tag) => new MockElement(tag)
};
global.window = {};

eval(js);

// Now test with live fetch
async function test() {
  const resp = await fetch('http://127.0.0.1:8080/api/documents?tree=true');
  const data = await resp.json();
  console.log('Fetched root_path:', data.root_path);
  console.log('Tree children count:', data.tree.children.length);

  window.docsRootPath = data.root_path;
  window.cachedDocs = data.docs;
  window.cachedTree = data.tree;

  try {
    renderDocTree();
    console.log('renderDocTree succeeded!');
    console.log('docList child count:', docElements['docList'].children.length);
  } catch (err) {
    console.error('renderDocTree failed:', err);
  }
}

test();
