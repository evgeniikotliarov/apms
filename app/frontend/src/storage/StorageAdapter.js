export default class StorageAdapter {
  constructor() {
    this.storage = sessionStorage;
  }

  loadData = (key) => {
    const rawData = this.storage.getItem(key);
    return JSON.parse(rawData);
  };

  saveData = (key, data) => {
    const parsedData = JSON.stringify(data);
    this.storage.setItem(key, parsedData)
  };
};
