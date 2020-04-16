$(function () {
  $("form#cssify-form").submit(function () {
    var xpath = $("#xpath").val(),
      response = $("#response"),
      css;
    response.html("");
    if (xpath.length === 0) {
      return false;
    }

    $.ajax({
      url: "https://us-central1-cssify.cloudfunctions.net/cssify",
      type: "GET",
      data: { xpath: xpath },
      success: function (data) {
        if (typeof data.response != "undefined") {
          if (data.status != "pass") {
            response.addClass("fail");
            response.html(data.response);
          } else {
            response.removeClass("fail");
            css = $("<input>");
            css
              .attr("type", "text")
              .attr("id", "css")
              .attr("readonly", true)
              .val(data.response);
            response.html("<br>Success! Your CSS:<br>");
            response.append(css);
            css.select();
          }
        } else {
          response.addClass("fail");
          response.text("unexpected failure");
        }
      },
    });
    return false;
  });
});
