$.feature('f_admin_users', function() {
  $('.js-filter-form-control').on('change', function() {
    $(this).closest('form').submit();
  });
});
