$.feature('f_jobs_add_edit', function () {
  var wrapper = $('.js-add-tags');

  var btn = wrapper.find('.js-add-tags-btn');
  var input = wrapper.find('.js-add-tags-value')
  var inputs = wrapper.find('.js-add-tags-inputs');

  btn.on('click', function () {
    var title = input.val().trim();
    input.val('');

    if (title.length === 0) {
      return;
    }

    $.post(wrapper.data('url'), {
      'title': title,
    }, function (html) {
      var html = $(html);
      var tag_id = html.data('tag_id');
      var existing = inputs.find('[data-tag_id=' + tag_id + ']');

      if (existing.length > 0) {
        // Check the existing one; don't append.
        existing.find('input').prop('checked', true);
      } else {
        inputs.append(html);
      }
    });
  });

  input.on('keypress', function (e) {
    // Don't submit the surrounding <form/>; click our local button.
    if (e.keyCode === 13) {
      btn.click();
      e.preventDefault();
    }
  });
});
