var pipeline = pipeline || {};

pipeline.BlurbFormViewModel = function() {
  var self = this;
  self.attachments = ko.observable(0);

  self.attachments.subscribe(function (newValue) {
    $('#id_document_set-TOTAL_FORMS').val(newValue);
  });

  self.addAttachment = function() {
    self.attachments(self.attachments() + 1);
  };
};

$(function() {
  ko.applyBindings(new pipeline.BlurbFormViewModel());
});
