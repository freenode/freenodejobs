$.feature('f_jobs_view', function() {
  $('.js-job-type').on('change', function() {
    $(this).closest('form').submit();
  });
});
