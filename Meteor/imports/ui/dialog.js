import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { Accounts } from 'meteor/accounts-base';
import { set_dialog_action } from './body';

import './sign-up-dialog.html';

Template.dialog.onRendered(function () {
    dialog = document.querySelector('.sign-up-dialog');
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
});


Template.dialog.events({
    'click button[action="New"]': function () {
        var target = $( event.target );
        event.preventDefault();
        event.stopPropagation();
        var username = $('dialog input#username').val();
        var password = $('dialog input#password').val();

        Accounts.createUser({username: username, password: password}, function (err) {
            if (err) {
                // Registration error
                message = _.isString(err.reason) ? err.reason : err.message;
                if (message.startsWith('Username')) {
                    $('dialog #name-error').text(message);
                    $('.username-input').toggleClass('is-invalid', true);
                } else if (message.indexOf('assword') > -1) {
                    $('dialog #pass-error').text(message);
                    $('.password-input').toggleClass('is-invalid', true);
                }
            } else {
                // Success. Account has been created and the user
                // has logged in successfully.
                $('.username-input').toggleClass('is-invalid', false);
                $('.password-input').toggleClass('is-invalid', false);

                Meteor.call('briefs.create', [], function (error, result) {
                    hide_dialogs();
                    FlowRouter.go('editBrief');
                });
            }
        });
    },
    'click button[action="Log in"]': function () {
        event.preventDefault();
        event.stopPropagation();
        var username = $('dialog input#username').val();
        var password = $('dialog input#password').val();

        $('.username-input').toggleClass('is-invalid', false);
        $('.password-input').toggleClass('is-invalid', false);
        if (username == undefined || username == ''){
            $('dialog #name-error').text('Username may not be empty');
            $('.username-input').toggleClass('is-invalid', true);
            $('.username-input').toggleClass('is-dirty', true);
            return;
        }
        Meteor.loginWithPassword(username, password, function (err) {
            if (err) {
                message = err.reason.toString();
                if (message.indexOf('User') > -1) {
                    $('dialog #name-error').text(message);
                    $('.username-input').toggleClass('is-invalid', true);
                } else if (message.indexOf('assword') > -1) {
                    $('dialog #pass-error').text(message);
                    $('.password-input').toggleClass('is-invalid', true);
                }
            } else {
                $('dialog #password').val('');
                $('dialog .password-input').toggleClass('is-dirty', false);
                hide_dialogs();
                FlowRouter.go('brief', {briefName: Meteor.user().username});
            }
        });
    },
    'click #new-brief-button': function () {
        set_dialog_action('New');
    },
    'click #login': function (event) {
        event.preventDefault();
        set_dialog_action('Log in');
        if (!dialog.open) {dialog.showModal()}
    }
});

export function hide_dialogs() {
    $(".mdl-dialog").each(function () {
        if (this.hasAttribute('open'))
            this.close();
    });
}