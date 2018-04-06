/*global
  $
*/

$.extend({
  feature: function(body_class, callback) {
    $(function() {
      if ($('body').hasClass(body_class)) {
        callback();
      }
    });
  }
});
