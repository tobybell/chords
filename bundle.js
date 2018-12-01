const fs = require("fs");
const fsa = require("./fsa");

const alpha = 'abcdefghijklmnopqrstuvwxyz';

async function loadAll() {
  const all = [];
  for (let i = 0; i < 26; i += 1) {
    for (let j = 0; j < 26; j += 1) {
      const pre = alpha[i] + alpha[j];
      const inPath = 'chords/' + pre + '.json';
      if (!await fsa.exists(inPath)) {
        continue;
      }
      console.log(pre);
      try {
        const chords = await fsa.load(inPath);
        all.push(...chords);
      } catch (e) {
        console.log('failed');
      }
    }
  }
  return all;
}


function unique(str) {
  let u = "";
  for (let i = 0; i < str.length; i += 1) {
    if (u.indexOf(str[i]) == -1) {
      u += str[i];
    }
  }
  return u;
}


async function main() {
  const all = await loadAll();
  const data = all.map(x => x.chords.map(x => x.trim()).join(",")).join("\n");
  fs.writeFileSync('bundle.txt', data, 'utf8');
  console.log(unique(data));
}

main();
