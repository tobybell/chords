const ug = require("ultimate-guitar-scraper");

function search(query) {
  return new Promise((resolve, reject) => {
    ug.search({ query, type: 'Chords' }, (err, tabs) => {
      if (err) {
        reject(err)
      } else {
        resolve(tabs);
      }
    })
  });
}

function get(url) {
  return new Promise((resolve, reject) => {
    ug.get(url, (err, tab) => {
      if (err) {
        reject(err);
      } else {
        resolve(tab);
      }
    })
  });
}

module.exports = {
  search,
  get,
};
