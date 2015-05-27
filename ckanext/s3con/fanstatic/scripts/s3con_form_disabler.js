"use strict";
ckan.module('s3con-form-disabler', function ($, _){
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
        $('.disablable').attr('readonly', false);
      } else {
        $('.disablable').attr('readonly', true);
      }
    },

  };
});