class BaseError extends Error {
  message() {
    throw new Error('You have to implement the method doSomething!');
  }
}

export class AuthenticationError extends BaseError {
  message() {
    return "Authorization error, please re log in"
  }
}

export class TokenExpiredError extends BaseError {
  message() {
    return "Your token is expired, please re log in"
  }
}

export class AuthorizatedError extends BaseError {
  message() {
    return "You don't have grant to this operation"
  }
}

export class ServerError extends BaseError {
  message() {
    return "Oops"
  }
}