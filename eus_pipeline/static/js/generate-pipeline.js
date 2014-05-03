ko.bindingHandlers.hidden = {
  update: function(element, valueAccessor) {
    var hide = ko.unwrap(valueAccessor());
    ko.bindingHandlers.visible.update(element, function() { return !hide; });
  }
};

var pipeline = pipeline || {};

pipeline.Category = function(name) {
  var self = this;

  self.name = ko.observable(name);
  self.blurbs = ko.observableArray();
  self.editing = ko.observable(false);

  self.startEditing = function() {
    self.editing(true);
  };
};

pipeline.GeneratorViewModel = function(approvedBlurbs) {
  var self = this;

  self.blurbs = ko.observableArray(JSON.parse(approvedBlurbs));
  self.categories = ko.observableArray();

  self.addCategory = function() {
    var name = prompt('Category name', '');
    if (name) {
      self.categories.push(new pipeline.Category(name));
    }
  };

  self.removeCategory = function(category) {
    if (!category.editing()) {
      self.categories.remove(category);
      self.blurbs.push.apply(self.blurbs, category.blurbs());
    }
  };

  self.events = ko.observableArray();
  self.newEventText = ko.observable('');

  self.addEvent = function() {
    if (self.newEventText().trim() !== '') {
      var lines = self.newEventText().split('\n');
      self.events.push({
        title: lines[0],
        description: lines.slice(1).join('<br/>')
      });
    }
    self.newEventText('');
  };

  self.removeEvent = function(event) {
    self.events.remove(event);
  };

  self.pipeline = ko.computed(function() {
    var headers = self.categories().map(function(category) {
      return {
        title: category.name(),
        blurbs: category.blurbs().map(function (blurb) { return blurb.id; })
      }
    });
    var events = self.events().map(function(event, index) {
      return {
        index: index + 1,
        title: event.title,
        lines: event.description.split('<br/>')
      }
    });
    return JSON.stringify({headers: headers, events: events});
  });
};
