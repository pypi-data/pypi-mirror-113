// Copyright (c) Jelmer Bot
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import App from './App.svelte';
import './assets/flexbox-shrink-patch.css';


export class StadModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: StadModel.model_name,
      _model_module: StadModel.model_module,
      _model_module_version: StadModel.model_module_version,
      _view_name: StadModel.view_name,
      _view_module: StadModel.view_module,
      _view_module_version: StadModel.view_module_version,
      network: [[],[]],
      featureMode: false,
      selectedNodes: []
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers
  };

  static model_name = 'StadModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'StadView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class StadView extends DOMWidgetView {
  render() {
    new App({
      target: this.el,
      props: {
        model: this.model,
      },
    });
  }
}