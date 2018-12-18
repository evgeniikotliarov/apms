export default class StorageAdapter {
  constructor() {
    this.storage = sessionStorage;
  }

  getData = (key) => {
    this.storage.getItem(key);
  };

  setData = (key, data) => {
    this.storage.setItem(key, data)
  };
};
