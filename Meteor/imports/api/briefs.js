import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

export const Briefs = new Mongo.Collection('briefs');

if (Meteor.isServer) {
    Meteor.publish('briefs', function () {
        return Briefs.find({});
        //return Briefs.find({}, {"sort" : {'popularity' : 1}});
    });
}

Meteor.methods({
    'briefs.create'(sources) {
        check(sources, Array);

        const username = Meteor.user().username;
        const new_brief = {
            'name': username,
            'sources': sources,
            'type': 'user'
        };
        Briefs.insert(new_brief);
        return username;
    },

    'briefs.edit'(sources) {
        check(sources, Array);
        const username = Meteor.user().username;
        Briefs.update({'name' : username}, {$set: {sources : sources}});
        return username;
    },

    'briefs.addSource'(source) {
        check(source, String);
        const username = Meteor.user().username;
        Briefs.update({'name' : username}, {$addToSet: {sources : source}});
    },
    'briefs.addSourceToCustomBrief'(source, briefName) {
        check(source, String);
        check(briefName, String);
        //console.log(source);
        //console.log(briefName);
        if (Meteor.user().username != 'kennivich' || briefName == '') return;
        Briefs.update({'name' : briefName}, {$addToSet: {sources : source}});
    },
    'briefs.removeSource'(source, briefName) {
        check(source, String);
        if (briefName) {
            check(briefName, String);
            if (Meteor.user().username != 'kennivich') return;
        } else {
            briefName = Meteor.user().username;
        }
        /*
        if (Meteor.user() && Meteor.user().username != 'kennivich') {

        } else if (!briefName) {
            briefName = 'kennivich';
        }
        */
        //console.log(briefName)
        //console.log(source)
        Briefs.update({'name' : briefName}, {$pull: {sources : source}});
    },
    'briefs.visitBrief'(briefName) {
        check(briefName, String);
        Briefs.update({'name' : briefName}, {$inc: {popularity : 1}});
    },
    'briefs.setPopularity'(briefName, popularity) {
        check(briefName, String);
        if (Meteor.user().username != 'kennivich' || briefName == '' || !popularity) return;
        Briefs.update({'name': briefName}, {$set: {'popularity': Number(popularity)}})
    },
    'briefs.removeBrief'(briefName) {
        check(briefName, String);
        if (Meteor.user().username != 'kennivich' || briefName == '' || !popularity) return;
        // Delete user and his brief
    }
});
