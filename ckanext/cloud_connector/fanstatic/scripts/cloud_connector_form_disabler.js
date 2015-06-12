"use strict";
ckan.module('cloudconnector-form-disabler', function ($, _){
  return{
    initialize: function (){
      $.proxyAll(this, /_on/);
      var switcher = document.getElementById('cloud-enable');
      var provider = document.getElementById('cloud-storage-provider');

      this.switcher = switcher;
      this.provider = provider;
      this.tester   = $('.test-providers-conf', this.el);

      $(switcher).on('click', this._onChangeState);
      $(provider).on('change', this._onSelectProvider).trigger('change');
      this.tester.on('click', this._onTestConf).on('blur', function (event) {
        $(event.target).popover('destroy');
      });
      this._onChangeState(false);
    },

    _onChangeState: function(event){
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

    _onTestConf: function (event) {
      var target = $(event.target)
      var fset = target.closest('.provider-fieldset');
      var values = $('.required-for-testing', fset);
      var data = []
      values.each(function (i, el) {
          data.push(el.value);
      });
      var req = $.post(this.options.testUrl, {
        'values': data,
        'provider': this.provider.value
      }, 'json').
      done(function(data) {
          target.popover({
            title: data.status.toUpperCase(),
            content: data.message,
            placement: 'top'
          });
      }).
      fail(function(obj, status, message) {
          target.popover({
            title: status.toUpperCase(),
            content: message,
            placement: 'top'
          });
      }).
      always(function() {
        target.popover('show');
      });


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