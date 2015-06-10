"use strict";
ckan.module('cloudconnector-form-disabler', function ($, _){
  return{
    initialize: function (){
      $.proxyAll(this, /_on/);
      var switcher = document.getElementById('cloud-enable');
      var provider = document.getElementById('cloud-storage-provider');

      this.switcher = switcher;
      this.provider = provider;
      $(switcher).on('click', this._onChangeState);
      $(provider).on('change', this._onSelectProvider).trigger('change');
      this._onChangeState(false);
    },

    _onChangeState: function(e){
      var checked = this.switcher.checked;
      this.disabler(checked);
    },

    _onSelectProvider: function (event) {
      this.disabler(false);
      var currentFieldset = $('#fieldset-' + event.target.value);
      var activeFieldset = $('.provider-fieldset.active');
      currentFieldset.toggleClass('active');
      activeFieldset.toggleClass('active');
      this.disabler(this.switcher.checked);
    },

    disabler: function(checked){
      if (checked){
        $('.provider-fieldset.active .disablable').attr('disabled', false);
      } else {
        $('.provider-fieldset.active .disablable').attr('disabled', true);
      }
    },

  };
});