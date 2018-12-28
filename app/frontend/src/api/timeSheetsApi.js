import Rx from 'rxjs/Rx'
import axios from 'axios';

export default class TimeSheetsApi {
  constructor() {
    this.client = axios;
    this.client.defaults.headers.post['Content-Type'] = 'application/json';
    this.client.defaults.headers.post['Accept'] = 'application/json';
    this.client.defaults.headers.patch['Content-Type'] = 'application/json';
    this.client.defaults.headers.patch['Accept'] = 'application/json';
  }

  getTimeSheet(token, userId, year, month) {
    const data = {year, month};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          `/api/employees/${userId}/time-sheets`,
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
          `/api/employees/${userId}/time-sheets`,
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.status);
  }

  updateOneDayOfTimeSheet(token, timeSheetId, day, value) {
    const data = {value};
    return Rx.Observable
      .fromPromise(
        this.client.patch(
          `/api/time-sheets/${timeSheetId}/day/${day}`,
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map((response) => response.status);
  }

  getTimeSheets(token, year, month) {
    const data = {year, month};
    return Rx.Observable
      .fromPromise(
        this.client.post(
          '/api/employees/time-sheets',
          JSON.stringify(data),
          {headers: {Authorization: token}}
        )
      )
      .map(response => response.data);
  }
}
