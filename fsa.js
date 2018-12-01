const fs = require('fs');

function exists(path) {
  return new Promise((resolve) => {
    fs.exists(path, resolve);
  });
}

function save(obj, path) {
  return new Promise((resolve, reject) => {
    fs.writeFile(path, JSON.stringify(obj), 'utf8', (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

function load(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) {
        reject(err);
      } else {
        resolve(JSON.parse(data));
      }
    });
  });
}

module.exports = {
  exists,
  load,
  save,
};
