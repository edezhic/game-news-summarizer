import './stats_form.html';

import { Briefs } from '../../api/briefs.js';
import { Template } from 'meteor/templating';


Template.stats_form.onCreated(function () {
    var instance = this;
    
});


Template.stats_form.helpers({
    briefs(){
        var username = Meteor.user() ? Meteor.user().username : '';
        return Briefs.find({'name' : {$ne : username}}, {"sort" : {'popularity' : -1, 'type': 1}});
    }
});

Template.stats_form.events({
    'click button[action="savePopularity"]': function (event) {
        var name = $(event.currentTarget).attr('name');
        var popularity = $('#briefPopularity[name="' + name + '"]').val();
        console.log(name);
        console.log(popularity);
        Meteor.call('briefs.setPopularity', name, popularity);
    },
    'click button[action="removeBrief"]': function (event) {
        var name = $(event.currentTarget).attr('name');
        console.log(name);
        Meteor.call('briefs.removeBrief', name);
        /*
        if (name) {
            Meteor.call('sources.setType', name, 'rss');
            console.log('Set ' + name + ' type rss');
            $('.titles').removeAttr('source');
        }
        titlesDep.changed();
        */
    },
});

