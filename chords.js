const fsa = require("./fsa");

const alpha = 'abcdefghijklmnopqrstuvwxyz';

function process(tab) {
  const text = tab.content.text;
  const chords = (text.match(/\[ch\]([^\[]+)/g) || []).map(x => x.substr(4));
  const res = {...tab};
  delete res.content;
  res.chords = chords;
  return res;
}

async function main() {
  for (let i = 0; i < 26; i += 1) {
    for (let j = 0; j < 26; j += 1) {
      const pre = alpha[i] + alpha[j];
      const inPath = 'tabs/' + pre + '.json';
      const outPath = 'chords/' + pre + '.json';
      if (!await fsa.exists(inPath) || await fsa.exists(outPath)) {
        continue;
      }
      console.log(pre);
      try {
        const tabs = await fsa.load(inPath);
        const chords = tabs.map(process);
        await fsa.save(chords, outPath);
      } catch (e) {
        console.log('failed');
        console.log(e);
      }
    }
  }
}

main();
