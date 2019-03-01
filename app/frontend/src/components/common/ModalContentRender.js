import React from 'react';

export default class BaseModalContentRender {
  dialog = null;

  setDialog(dialog) {
    this.dialog = dialog;
  }

  head() {
    return null;
  }

  content() {
    return null;
  }

  foot() {
    return null;
  }
}