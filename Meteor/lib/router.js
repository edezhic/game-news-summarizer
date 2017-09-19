FlowRouter.route('/', {
    action: function () {
        FlowRouter.go('brief', {briefName: 'Home'});
    }
});

FlowRouter.route('/b::briefName', {
    name: 'brief',
    triggersEnter: [function (context) {
        //console.log(context.params.briefName);
        Meteor.call('briefs.visitBrief', context.params.briefName);
    }],
    action: function() {
        BlazeLayout.render("body_layout", {content: "summaries_grid"});
    }
});

FlowRouter.route('/source::sourceName', {
    name: 'source',
    action: function() {
        BlazeLayout.render("body_layout", {content: "summaries_grid"});
    }
});

FlowRouter.route('/topic::topicName', {
    name: 'topic',
    action: function() {
        BlazeLayout.render("body_layout", {content: "summaries_grid"});
    }
});

FlowRouter.route('/search::searchQuery', {
    name: 'search',
    action: function() {
        BlazeLayout.render("body_layout", {content: "summaries_grid"});
    }
});

FlowRouter.route('/editBrief', {
    name: 'editBrief',
    action: function() {
        if (Meteor.user()) {
            BlazeLayout.render("body_layout", {content: "edit_brief_form"});
        } else {
            //BlazeLayout.render("body_layout", {content: "edit_brief_form"});
            FlowRouter.go('brief', {briefName: 'Home'});
        }
    }
});

FlowRouter.route('/stats', {
    name: 'stats',
    action: function() {
        BlazeLayout.render("body_layout", {content: "stats_form"});
    }
});
