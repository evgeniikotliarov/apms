export default class StorageAdapter {
  constructor() {
    this.storage = sessionStorage;
  }

  loadData = (key) => {
    const rawData = this.storage.getItem(key);
    const data = JSON.parse(rawData);
    return data? data : {};
  };

  saveData = (key, data) => {
    const parsedData = JSON.stringify(data);
    this.storage.setItem(key, parsedData);
  };

  removeData = (key) => {
    this.storage.removeItem(key);
  };
};
