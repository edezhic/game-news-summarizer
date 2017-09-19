import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { Briefs } from '../api/briefs.js';
import { Sources } from '../api/sources.js';
import { check } from 'meteor/check';

export const Summaries = new Mongo.Collection('summaries');
const Links = new Mongo.Collection('links');

if (Meteor.isServer) {
    Meteor.publish('summaries', function (type, name, limit) {
        var sources = [];

        if (type == 'brief'){
            var brief = Briefs.findOne({'name': name});
            if (brief) {sources = brief.sources;}
        } else if (type == 'source') {
            sources = [name]
        } else if (type == 'topic') {
            var cursor = Sources.find({'topics': name});
            cursor.forEach(function (doc) {
                sources.push(doc.name);
            });
        } else if (type == 'search') {
            search_query = {$or: [{'title': {$regex : new RegExp(name, "i")}}, {'text': {$regex : new RegExp(name, "i")}}]};
            return Summaries.find(search_query, {'sort' : {'_id' : -1}, 'limit' : limit});
        }

        return Summaries.find({'source': {$in: sources}}, {'sort' : {'_id' : -1}, 'limit' : limit});
    });


    Meteor.publish('source_summaries', function (source) {
        var sources = [];
        return Summaries.find({'source': source}, {'sort': {'_id': -1}, 'limit': 3});
    });
}

Meteor.methods({
    'summaries.deleteSummary'(id) {
        check(id, String);
        if (!Meteor.user().username === 'kennivich') return;
        
        var url = Summaries.findOne({'_id': new Meteor.Collection.ObjectID(id)}).url;

        Links.remove({'url': url});
        Summaries.remove({'url': url});
    },
    'summaries.inc_counter'(url) {
        check(url, String);
        Summaries.update({'url': url},{$inc: {visits : 1}})
    }
});
