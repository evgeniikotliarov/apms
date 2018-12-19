import Rx from 'rxjs/Rx';
import axios from 'axios';

export default class TimeSheetsApi {
  constructor() {
    this.client = axios;
    this.client.defaults.headers.post['Content-Type'] = 'application/json';
    this.client.defaults.headers.post['Accept'] = 'application/json';
  }

  getTimeSheet(token, userId, year, month) {
    const data = {year, month};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          `api/${userId}/time-sheets`,
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.data);
  }

  updateTimeSheet(token, userId, year, month, sheet) {
    const data = {year, month, sheet};
    return Rx.Observable
      .fromPromise(
        this.client.patch(
          `api/${userId}/time-sheets`,
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.data);
  }

  getTimeSheets(token, year, month) {
    const data = {year, month};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          `api/employees/time-sheets`,
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.data);
  }
}