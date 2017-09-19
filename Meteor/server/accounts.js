import { Accounts } from 'meteor/accounts-base';
import { Briefs } from '../imports/api/briefs.js';
import { check } from 'meteor/check';


Accounts.validateNewUser(function (user) {
    var username = user.username;

    check(username, String);
    const nameRegex = /^[a-zA-Z0-9]+$/;
    const nameValidation = username.match(nameRegex);
    if (nameValidation == null) {
        throw new Meteor.Error('Username is not valid');
    }

    const brief = Briefs.findOne({'name': username});
    if (brief != undefined) {
        throw new Meteor.Error('Username already exists');
    }

    if (username.length < 2) {throw new Meteor.Error('Username is too short (need at least 2 characters)')}
    else if (username.length > 14) {throw new Meteor.Error('Username is too long (no more than 14 characters)')}

    if (user.username)
        return true;
    throw new Meteor.Error("Something went wrong...");
});