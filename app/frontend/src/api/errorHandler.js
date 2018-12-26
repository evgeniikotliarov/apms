import {
  AuthenticationError,
  AuthorizatedError,
  ServerError,
  TokenExpiredError
} from "../errors/errors";

export default class ErrorHandler {
  static handle(responseCode) {
    // console.log(responseCode);
    if (responseCode >= 500)
      ErrorHandler.handleServerError(responseCode);
    if (responseCode >= 400)
      ErrorHandler.handleUserError(responseCode);
  }

  static handleUserError(code) {
    if (code === '401 Unauthorized')
      throw new AuthenticationError();
    if (code === '401 Token expired')
      throw new TokenExpiredError();
    if (code === '403 Forbidden')
      throw new AuthorizatedError();
  }

  static handleServerError(code) {
    if (code === 500)
      throw new ServerError();
  }
}