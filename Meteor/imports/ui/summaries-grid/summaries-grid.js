import './summaries-grid.html';
import { Summaries } from '../../api/summaries.js';

var subcription;
var instance;

Template.summaries_grid.onCreated(function () {

    // 1. Initialization
    instance = this;
    instance.loaded = new ReactiveVar(0);
    instance.limit = new ReactiveVar(12);

    // will re-run when the "limit" reactive variables changes
    instance.autorun(function () {

        var limit = instance.limit.get();

        FlowRouter.watchPathChange();
        //console.log("Asking for "+limit+" posts…")

        var type = FlowRouter.getRouteName();
        var value;
        if (type == 'brief') {
            value = FlowRouter.current().params.briefName;
        } else if (type == 'source') {
            value = FlowRouter.current().params.sourceName;
        } else if (type == 'topic') {
            value =  FlowRouter.current().params.topicName;
        } else if (type == 'search') {
            value = FlowRouter.current().params.searchQuery;
        }

        subscription = instance.subscribe('summaries', type, value, limit);

        // if subscription is ready, set limit to newLimit
        if (subscription.ready()) {
            //console.log("> Received "+limit+" posts. \n\n")
            instance.loaded.set(limit);
        } else {
            //console.log("> Subscription is not ready yet. \n\n");
        }
    });

    instance.summaries = function() {
        return Summaries.find({}, {limit: instance.loaded.get()});
    }

    instance.no_summaries = function () {
        return Summaries.find({}).count() == 0 && subscription.ready();
    }

});


Template.summaries_grid.onRendered(function () {
    instance.loaded = new ReactiveVar(0);
    instance.limit = new ReactiveVar(12);
});


Template.summaries_grid.helpers({
    summaries() {
        // Add dividers to summaries
        var summaries = [];
        var divider_values = [6, 12, 24, 48];

        //Summaries.find({}, {limit: Session.get("limit")}).forEach(function (summary) {
        Template.instance().summaries().forEach( function (summary) {
            var difference = Math.floor((Date.now()/1000 - summary.date)/3600);
            var max_diff = 0;
            divider_values.forEach(function (value) {
                if (difference > value) {
                    max_diff = value;
                    divider_values = _.filter(divider_values, function (val) {return val > max_diff})
                }
            });
            if (max_diff) {summary.divider = max_diff;}
            summaries.push(summary);
        });
        return summaries;
    },
    loading() {
        if (Template.instance().no_summaries()) return false;
        return !Template.subscriptionsReady
    },
    notFound() {
        //TODO: Show picture Not Found
        return Template.instance().no_summaries()
    },
    userEmptyBrief() {
        var no_summries = Template.instance().no_summaries();
        if (Meteor.user() && Meteor.user().username == FlowRouter.current().params.briefName)
            return no_summries;
        else
            return false;
    }
});


Template.summaries_grid.events({
    'click #removeCUSource': function (event) {
        var source = $(event.currentTarget).attr('source');
        Meteor.call('briefs.removeSource', source);
        //instance.limit.set(_.min([instance.limit.get() - 1, instance.count()]));
        instance.limit.set(instance.limit.get() == 12 ? 11 : 12);
    },
    'click #scroll_up': function () {
        document.body.scrollTop = document.documentElement.scrollTop = 0;
    }

});

$(window).scroll(function () {
    loadMore();
    if (document.body.scrollTop > 100) {
        $('#scroll_up').fadeIn(500);
    } else {
        $('#scroll_up').fadeOut(150);
    }
});

function loadMore() {
        var threshold, target = $("#loading-spinner");
        if (!target.length) return;

        threshold = $(window).scrollTop() + $(window).height() - target.height();
        //console.log(target.offset().top.toString() + ' < ' + threshold.toString());
        if (target.offset().top < threshold) {

            if (!target.data("visible")) {
                target.data("visible", true);
                var limit = instance.limit.get();
                // increase limit by 5 and update it
                limit += 12;
                instance.limit.set(limit);
            }
        } else {
            if (target.data("visible")  ) {
                target.data("visible", false);
            }
        }
}