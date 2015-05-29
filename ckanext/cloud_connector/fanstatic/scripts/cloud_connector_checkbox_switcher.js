"use strict";

ckan.module('s3con-checkbox-switcher', function ($, _) {
  return {
    initialize: function(){
      $.proxyAll(this, /_on/);
      this.checkbox = $(".col-toggle input");
      this.checkbox.on("change", this._onChange);
      this.checkbox.trigger("change");
    },

    checkbox: undefined,

    _onChange: function(e){
      var that = this.checkbox;
      if (that.prop("checked")) {
        that.parent().addClass("active");
      } else {
        that.parent().removeClass("active");
      }
    },
    
  }
});
