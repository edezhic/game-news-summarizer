import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { Accounts } from 'meteor/accounts-base';
import { hide_dialogs } from './../dialog';
import { set_dialog_action } from '../body';

import './help-dialogs.html';

Template.help_dialogs.onRendered(function () {
    $(".help-dialog").each(function () {
        if (!this.showModal)
            dialogPolyfill.registerDialog(this);
    });

    Tracker.autorun(function() {
        //console.log(Template.help_dialogs.rendered);
        //// OPEN DIALOGS ON DIFFERENT PATHS
        FlowRouter.watchPathChange();
        if (!FlowRouter.current().route )//|| )
            return;
        var cookies = new Cookies();
        var routeName = FlowRouter.current().route.name;

        var currentDialog;
        //console.log(cookies.has('first-time'));
        if (!cookies.has('first-time') && routeName == 'brief' && !Meteor.user()) {
            currentDialog = $('.help-dialog#first')[0];
            cookies.set('first-time', true);
        }

        if (!cookies.has('first-loggedin-brief') && routeName == 'brief' && Meteor.user()) {
            currentDialog = $('.help-dialog#loggedinBrief')[0];
            cookies.set('first-loggedin-brief', true);
        }


        if (!cookies.has('first-editBrief') && routeName == 'editBrief' ) {
            currentDialog = $('.help-dialog#editBrief')[0];
            cookies.set('first-editBrief', true);
        }

        hide_dialogs();
        if (currentDialog && !currentDialog.open) {currentDialog.showModal()}

        // DEBUG ONLY
        //cookies.remove('first-time');
        //cookies.remove('first-editBrief');
        //cookies.remove('first-loggedin-brief');
    });

});

Template.help_dialogs.events({
    'click button[action="close"]': function (event) {
      hide_dialogs();
    },
    'click #new-brief-button': function () {
        console.log('click');
        set_dialog_action('New');
    }
});




