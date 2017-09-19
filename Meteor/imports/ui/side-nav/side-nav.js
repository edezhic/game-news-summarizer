import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { Briefs } from '../../api/briefs';
import { toggle_side_nav, set_dialog_action } from '../body';

import './side-nav.html';

Template.side_nav.helpers({
    defaultBriefs() {
        var username = Meteor.user() ? Meteor.user().username : '';
        return Briefs.find({'name' : {$ne : username}}, {"sort" : {'popularity' : -1, 'type': 1}, 'limit': 15});
    }
});

Template.side_nav.events({
    'click #new-brief-button': function () {
        set_dialog_action('New');
    },
    'click #logout': function(event){
        event.preventDefault();
        Meteor.logout();
    },
    'click .brief-nav a': function () {
        toggle_side_nav('close');
    },
    'click #edit-brief-button': function () {
        //go to edit brief page
        FlowRouter.go('editBrief');
        toggle_side_nav('close');
    }
});