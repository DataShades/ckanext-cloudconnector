"use strict";
ckan.module('cloudconnector-form-disabler', function ($, _){
  return{
    initialize: function (){
      $.proxyAll(this, /_on/);
      var switcher = document.getElementById('cloud-enable');
      this.switcher = switcher;
      $(switcher).on('click', this._onChangeState);
      this._onChangeState(false);
    },

    _onChangeState: function(e){
      var checked = this.switcher.checked;

      if (checked){
        $('.disablable').attr('disabled', false);
      } else {
        $('.disablable').attr('disabled', true);
      }
    },

  };
});