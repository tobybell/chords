const fsa = require("./fsa");

const alpha = 'abcdefghijklmnopqrstuvwxyz';

function checkTab(tab) {
  tab.chords.forEach(x => checkChord(cleanChord(x), tab));
}

function cleanChord(str) {
  // Replace H chords with B chords, since this is apparently something they
  // do in Spain.
  if (str[0] == 'H') {
    str = 'B' + str.substr(1);
  }

  // Replace M7 with maj7.
  if (str.endsWith('M7')) {
    str = str.substr(0, str.length - 2) + 'maj7';
  }

  // Replace sus with sus4.
  if (str.endsWith('sus')) {
    str = str.substr(0, str.length - 3) + 'sus4';
  }

  return str;
}

function checkChord(str, tab) {
  if (!/^[A-G][#b]?(m|dim|)(5|6|7|maj7|9|add9|sus2|sus4)?(\/[A-G][#b]?)?$/.test(str)) {
    console.log(str, tab.url);
  }
}

async function main() {
  for (let i = 0; i < 26; i += 1) {
    for (let j = 0; j < 26; j += 1) {
      const pre = alpha[i] + alpha[j];
      const inPath = 'chords/' + pre + '.json';
      if (!await fsa.exists(inPath)) {
        continue;
      }
      try {
        const tabs = await fsa.load(inPath);
        const chords = tabs.forEach(checkTab);
      } catch (e) {
        console.log('failed');
      }
    }
  }
}

main();
