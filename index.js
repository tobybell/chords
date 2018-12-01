const fsa = require("./fsa");
const api = require("./api");

const alpha = 'abcdefghijklmnopqrstuvwxyz';

async function scrape(pre) {
  const tabs = await api.search(pre);
  return Promise.all(tabs.map(x => api.get(x.url)));
}

async function main() {
  for (let i = 0; i < 26; i += 1) {
    for (let j = 0; j < 26; j += 1) {
      const pre = alpha[i] + alpha[j];
      const path = 'tabs/' + pre + '.json';
      if (await fsa.exists(path)) {
        continue;
      }
      console.log(pre);
      try {
        const res = await scrape(pre);
        await fsa.save(res, 'tabs/' + pre + '.json');
      } catch (e) {
        console.log('failed');
      }
    }
  }
}

main();
