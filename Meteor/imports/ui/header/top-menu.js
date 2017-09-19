import './top-menu.html';
import { Template } from 'meteor/templating';
import { toggle_side_nav, set_dialog_action } from '../body';
import { Briefs } from '../../api/briefs';

Template.top_menu.events({
    'click #nav-button': toggle_side_nav,
    'click #login': function (event) {
        event.preventDefault();
        set_dialog_action('Log in');
        if (!dialog.open) {dialog.showModal()}
    }
});

Template.top_menu.helpers({
    page_headline() {
        FlowRouter.watchPathChange();
        var value;
        var type = FlowRouter.getRouteName();

        if (type == 'brief') {
            type = 'B';
            value = FlowRouter.current().params.briefName;
        } else if (type == 'source') {
            value = FlowRouter.current().params.sourceName;
        } else if (type == 'topic') {
            value =  FlowRouter.current().params.topicName;
        } else if (type == 'search') {
            value = FlowRouter.current().params.searchQuery;
        } else if (type == 'editBrief') {
            type = 'edit';
            value = Meteor.user().username;
        } else if (type == 'stats') {
            document.title = 'Stats';
            return "<span class='mdl-color-text--pink-100'>Stats</span>";
        }
        document.title = value;

        return type + ": <span class='mdl-color-text--pink-100'>" + value + '</span>';
    },
    hot_briefs() {
        var username = Meteor.user() ? Meteor.user().username : '';
        //console.log((window.innerWidth > 0) ? window.innerWidth : screen.width);
        var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
        var limit = (width > 1000) ? 3 : 1;
        var hot_briefs = Briefs.find({'name' : {$ne : username}}, {"sort" : {'popularity' : -1, 'type': 1}, 'limit': limit});
        if (hot_briefs) {
            return hot_briefs;
            //return hot_brief.name;
        }
    }
});