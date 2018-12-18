export default class StorageAdapter {
  constructor() {
    this.storage = sessionStorage;
  }

  loadData = (key) => {
    this.storage.getItem(key);
  };

  saveData = (key, data) => {
    this.storage.setItem(key, data)
  };
};
