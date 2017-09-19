import { Summaries } from '../imports/api/summaries';
import { Briefs } from '../imports/api/briefs';

var increaseVisits = new ScheduledTask('every 10 min', function () {
    console.log("increaseVisits task was run.");
    var yesterday = new Date(new Date().getTime() - (6 * 60 * 60 * 1000)) / 1000;
    var increase;

    Summaries.find({'date': {$gte: yesterday}}).forEach(function(mydoc) {
        if (!mydoc.visits || mydoc.visits < 5)
            increase = Math.floor((Math.random() * 3));
        else if (mydoc.visits < 50)
            increase = Math.floor((Math.random() * Math.floor(mydoc.visits / 3.0 + 1)));
        else
            increase = Math.floor((Math.random() * 3));
        Summaries.update({_id: mydoc._id}, {$inc: {visits: increase}})
    });
});
increaseVisits.start();

// Delete posts > 21 days old
var removeOldPosts = new ScheduledTask('at 7:00 am', function () {
    console.log("removeOldPosts task was run.");
    var threeWeeksAgo = new Date(new Date().getTime() - (24 * 60 * 60 * 1000 * 21)) / 1000;
    console.log(Summaries.find({'date': {$lte: threeWeeksAgo}}).count());
    Summaries.remove({'date': {$lte: threeWeeksAgo}});
});
removeOldPosts.start();

var popularityRecalculate = new ScheduledTask('at 6:00 am', function () {
    console.log("popularityRecalculate task was run.");
    var new_value;
    Briefs.find({}).forEach(function(mydoc) {
        if (mydoc.popularity) {
            new_value = Math.floor(mydoc.popularity * 0.8);
            Briefs.update({_id: mydoc._id}, {$set: {popularity: new_value}})
        }
    });
});
popularityRecalculate.start();