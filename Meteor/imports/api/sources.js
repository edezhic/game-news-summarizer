import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

export const Sources = new Mongo.Collection('sources');

if (Meteor.isServer) {
    // This code only runs on the server
    Meteor.publish('sources', function () {
        return Sources.find({});
    });
}

Meteor.methods({
    'sources.addSource'(name, url) {
        check(name, String);
        check(url, String);
        if (name.length < 2 || url.length < 2) {return}
        var patt = new RegExp("^[a-zA-Z0-9_.:-]*$");
        //var res = patt.test(str);
        if (patt.test(name) == false) {
            return 'Allowed characters: a-z 0-9 : - _ . ';
        }

        if (Sources.findOne({name: name}) == undefined) {
            Meteor.call('briefs.addSource', name);
            Sources.insert({name : name, type: 'user', url: url});
            return 'ok';
        } else {
            return 'That name is already taken';
        }
    },
    'sources.setTopic'(name, topics) {
        check(name, String);
        check(topics, Array);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.update({'name': name}, {$set: {'topics': topics}});
    },
    'sources.setUrl'(name, url) {
        check(name, String);
        check(url, String);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.update({'name': name}, {$set: {'url': url}});
    },
    'sources.setHidden'(name, hidden) {
        check(name, String);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.update({'name': name}, {$set: {'hidden': hidden}});
    },
    'sources.setType'(name, type) {
        check(name, String);
        check(type, String);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.update({'name': name}, {$set: {'type': type}});
    },
    'sources.setParams'(name, domain, home_url, params) {
        check(name, String);
        check(domain, String);
        check(home_url, String);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.update({'name': name}, {$set: {'domain': domain, 'home_url': home_url, 'params': params}});
    },
    'sources.removeSource'(name) {
        check(name, String);
        if (!Meteor.user().username === 'kennivich') return;
        Sources.remove({'name': name});
    }
});

