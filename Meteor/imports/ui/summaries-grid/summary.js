import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { Session } from 'meteor/session';

import './summary.html';

Template.summary.rendered = function () {
    var title_div = $(this);
    $(this.find('.with-img')).each(function () {
        var title_div = $(this);
        var img = new Image();
        var width, height;

        img.onload = function () {
            // check if width was set earlier, if not then set it now
            width = this.width;
            // do the same with height
            height = this.height;
            if (this.height < 100) {
                //console.log('Deleted: ');
                //console.log(this.src);
                $(title_div).toggleClass('with-img', false);
                $(title_div).css('background-image', '');
            }
            /*
            else if (this.height < 100) {
                $(title_div).toggleClass('with-img', false);
                $(title_div).toggleClass('no-flex-grow', true);
                $(title_div).css('background-image', '');
                $(title_div).before('<div class="card-thumbnail"><img src="' + this.src + '" /></div>');
            }
            */
        };
        // extract image source from css using one, simple regex
        // src should be set AFTER onload handler
        img.src = $(this).css('background-image').replace(/url\(['"]*(.*?)['"]*\)/g, '$1');
    });
};

Template.summary.helpers({
    currentUserBrief() {
        if (!Meteor.userId()) { return false;}
        var briefName = FlowRouter.getParam("briefName");
        if (briefName == undefined || briefName != Meteor.user().username) {
            return false;
        }
        return true;
    },
    notCurrentSource() {
        var sourceName = FlowRouter.getParam("sourceName");

        return sourceName != this.source;
    },
    disabled() {
        if (!Meteor.userId()) {
            return 'disabled';
        }
    },
    cardsDivider() {
        if (this.divider != undefined) {
            time = (this.divider != 1) ? ' hours ' : ' hour ';
            return '<div class="cards-divider"> > ' + this.divider + time + ' ago</div>';
        }
    },
});

Template.summary.events({
    'click .card-menu-button': function (event) {

        var button = $(event.currentTarget);
        var url = $(button).attr('id');
        var container = $('div[for="' + url + '"]');
        var width = $(container).children('.mdl-menu').width();
        var height = $(container).children('.mdl-menu').height() + 16;

        $(container).width(width);
        $(container).height(height);
        $(container).toggleClass('is-visible');
    },
    'click .goToSource': function (event) {
        var source = $(event.currentTarget).attr('source');
        FlowRouter.go('source', {sourceName: source }); 
        document.body.scrollTop = document.documentElement.scrollTop = 0; 
        $('.mdl-menu__container').toggleClass('is-visible', false);
        
    },
    'click .summary_link': function (event) {
        var url = $(event.currentTarget).attr('href');
        Meteor.call('summaries.inc_counter', url);
    }
});