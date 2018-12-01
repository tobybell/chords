const fsa = require('./fsa');

async function main() {
  const a = await fsa.load('tabs/iq.json');
  console.log(a);
}

main();
