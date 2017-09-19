import './edit-brief-form.html';

import { Briefs } from '../../api/briefs.js';
import { Sources } from '../../api/sources.js';
import { Summaries } from '../../api/summaries.js';
import { Template } from 'meteor/templating';

Meteor.subscribe('sources');
var summaries_subscription;

var website_params = ['title_path', 'content_path', 'img_path', 'img_prop', 'check_node', 'ignore_urls_with', 'ignore_urls_without', 'retain_params'];
var sourcesDep = new Deps.Dependency;
var titlesDep = new Deps.Dependency;
var current_source;

var userSources;

Template.edit_brief_form.onCreated(function () {
    var instance = this;
    instance.autorun(function () {
        summaries_subscription = instance.subscribe('source_summaries', '');
    });

    instance.summaries = function() {
        return Summaries.find({}, {limit: 3});
    }

    instance.no_summaries = function () {
        return Summaries.find({}).count() == 0 && summaries_subscription.ready();
    }
    switchTo('topics');

});


Template.edit_brief_form.helpers({
    topics() {
        var sources = Sources.find({});
        var topics = [];
        sources.forEach(function (source) {
            Array.prototype.push.apply(topics,source.topics)
        });
        return _.sortBy(_.uniq(topics), function (name) {return name});
    },
    Sources() {
        if (Meteor.user() && userSources == undefined) {
            var userBrief = Briefs.findOne({'name' : Meteor.user().username});

            if (userBrief != undefined) {
                userSources = userBrief.sources ? userBrief.sources : [];
            }
        }

        sourcesDep.depend();
        var topic = $('.sources').attr('topic');
        if (topic != undefined) {
            return Sources.find({topics: topic, hidden: {$ne: true}}, {sort: {name: 1}});
        } else if (userSources){
            return Sources.find({name: {$in: userSources}});
        } else {
            return [];
        }
    },
    userSourcesExist(){
        return Sources.find({type: 'user'}).count() > 0;
    },
    userSources(){
        sourcesDep.depend();
        return Sources.find({type: 'user'});
    },
    hiddenSourcesExist(){
        return Sources.find({hidden: true}).count() > 0;
    },
    hiddenSources(){
        sourcesDep.depend();
        return Sources.find({hidden: true});
    },
    zeroSourcesExist(){
        return Sources.find({zero_entries: true}).count() > 0;
    },
    zeroSources(){
        sourcesDep.depend();
        return Sources.find({zero_entries: true});
    },
    lastTitles() {
        titlesDep.depend();
        var sourceName = $('.titles').attr('source');
        if (sourceName) {
            if (Template.instance().no_summaries()) {
                $('.titles h6').html(sourceName + ' will be parsed soon');
            } else {
                $('.titles h6').html('Last titles on ' + sourceName);
            }
            if (summaries_subscription.ready()) {
                $('.titles .mdl-grid').fadeIn(50);
                return Template.instance().summaries();
            }

        }

        return []
    },
    text() {
        //console.log(this.text.slice(0, 200));
        //return this.text.slice(0, 200);
        if (this.text.length > 200) {
            return this.text.slice(0, 200) + '...';
        } else {
            return this.text;
        }
    },
    containsSource(name) {
        if (_.contains(userSources, name)) {
            return 'is-checked';
        }
    },
    source_url() {
        titlesDep.depend();
        if (current_source) {
            return current_source.url;
        }
    },
    source_topics() {
        titlesDep.depend();
        if (current_source && current_source.topics) {
            return current_source.topics.toString();
        } else {
            return '';
        }
    },
    isWebsite(){
        titlesDep.depend();
        return current_source && current_source.type == 'website'
    },
    params(){
        titlesDep.depend();
        return website_params;
        //return current_source.params.toString();
    },
    param(param_name){
        titlesDep.depend();
        if (current_source.params && current_source.params[param_name])
            return current_source.params[param_name];
        else
            return '';
    },
    domain() {
        titlesDep.depend();
        if (current_source.domain)
            return current_source.domain;
    },
    home_url() {
        titlesDep.depend();
        if (current_source.home_url)
            return current_source.home_url;
    }

});

Template.edit_brief_form.events({
    'click .topic': function (event) {
        var topic = $(event.currentTarget).attr('name');
        switchTo('sources');
        $('.sources').attr('topic', topic);
        sourcesDep.changed();
    },
    'click .return_to_topics button': function (event) {
        hideEverything();
        switchTo('topics');
    },
    'click .sources .sourceName': function (event, instance) {
        $('.sourceName').toggleClass('active', false);
        $(event.currentTarget).toggleClass('active', true);
        var source = $(event.currentTarget).attr('name');
        current_source = Sources.findOne({'name' : source});
        switchTo('titles', false);

        $('.titles').attr('source', source);
        summaries_subscription.stop();
        summaries_subscription = instance.subscribe('source_summaries', source);
        titlesDep.changed();

    },
    'click button[action="addSource"]': function (e) {
        event.preventDefault();
        event.stopPropagation();
        var sourceInputs = $('input[id*="source"]');
        var name = $('#sourceName').val();
        var url = $('#addSourceUrl').val();
        if (name.length < 2 || url.length < 2) {return}

        sourceInputs.prop('disabled', true);
        $('.edit_brief_form').append('<div class="mdl-spinner mdl-js-spinner is-active is-upgraded"><i class="material-icons">loop</i></div>');

        Meteor.call('sources.addSource', name, url, function (error, result) {
            if (result != 'ok') {
                $('#sourceName-error').text(result);
                $('#sourceName').parents('.mdl-textfield').toggleClass('is-invalid', true);
                sourcesDep.changed();
                //console.log(result);
            } else {
                sourceInputs.val('');
                sourceInputs.parents('.mdl-textfield').toggleClass('is-dirty', false);
                $('#sourceName').parents('.mdl-textfield').toggleClass('is-invalid', false);

                $('#sourceAdded').fadeIn(1000);
                setTimeout(function() { $('#sourceAdded').fadeOut(1000); }, 4000);
                userSources.push(name);
                sourcesDep.changed();
                //console.log(result);
            }
        });

        sourceInputs.prop('disabled', false);
        $('.mdl-spinner').remove();

    },
    'click .mdl-switch': function (event) {
        var target = $( event.currentTarget );
        var name = target.attr('name');
        event.preventDefault();
        event.stopPropagation();
        target.toggleClass('is-checked');
        if (target.hasClass('is-checked')) {
            Meteor.call('briefs.addSource', name);
        } else {
            Meteor.call('briefs.removeSource', name);
        }
    },
    // ADMIN FUNCTIONS
    'click button[action="saveSource"]': function (event) {
        var name = current_source.name;
        var topic = $('#sourceTopic').val();
        var url = $('#sourceUrl').val();
        var type = current_source.type;
        if (name && topic) {
            Meteor.call('sources.setTopic', name, [topic]);
        }
        if (name && url) {
            Meteor.call('sources.setUrl', name, url)
        }
        if (name && type == 'website'){
            var domain = $('input#domain').val();
            var home_url = $('input#home_url').val();
            var params = new Object();
            _.each(website_params, function (param) {
                var value = $('input#' + param).val();
                if (value == '') return;
                if (param == 'ignore_urls_with' || param == 'ignore_urls_without') {
                    params[param] = value.split(',');
                } else {
                    params[param] = value;
                }
            });
            console.log(params);
            Meteor.call('sources.setParams', name, domain, home_url, params);
        }

        //if ()
        //console.log(name + ' - ');
        //console.log([topic]);
    },
    'click button[action="hideSource"]': function (event) {
        var name = current_source.name;
        if (name) {
            Meteor.call('sources.setHidden', name, true);
            console.log('Set ' + name + ' hidden true');
        }
        sourcesDep.changed();
    },
    'click button[action="showSource"]': function (event) {
        var name = current_source.name;
        if (name) {
            Meteor.call('sources.setHidden', name, false);
            console.log('Set ' + name + ' hidden false');
        }
        sourcesDep.changed();
    },
    'click button[action="setSourceTypeRss"]': function (event) {
        var name = current_source.name;
        if (name) {
            Meteor.call('sources.setType', name, 'rss');
            console.log('Set ' + name + ' type rss');
            $('.titles').removeAttr('source');
        }
        titlesDep.changed();
    },
    'click button[action="setSourceTypeWebsite"]': function (event) {
        var name = current_source.name;
        if (name) {
            Meteor.call('sources.setType', name, 'website');
            console.log('Set ' + name + ' type website');
            $('.titles').removeAttr('source');
        }
        titlesDep.changed();
    },
    'click button[action="addSourceToCustomBrief"]': function (event) {
        var sourceName = current_source.name;
        var briefName = $('#addSourceToCustomBriefName').val();
        if (sourceName && briefName) {
            Meteor.call('briefs.addSourceToCustomBrief', sourceName, briefName);
            console.log('Added ' + sourceName + ' to ' + briefName);
        }
        
    },
    'click button[action="removeSource"]': function (event) {
        var name = current_source.name;
        if (name) {
            Meteor.call('sources.removeSource', name);
            $('.titles').removeAttr('source');
        }
        sourcesDep.changed();
        titlesDep.changed();
    },
    'click button[action="deleteSummary"]': function (event) {
        var id = $( event.currentTarget ).attr('id');
        Meteor.call('summaries.deleteSummary', id);
        titlesDep.changed();
        //console.log(id);
        //console.log(Summaries.findOne({'_id': new Meteor.Collection.ObjectID(id)}).url);
    }
    /*
     'click .column-check': function (event) {
     var target = $( event.currentTarget );
     event.preventDefault();
     event.stopPropagation();
     var column = target.parents('ul');
     var labels = column.children('li').children('label');
     var toggle = false;
     labels.each(function () {
     if ($(this).hasClass('is-checked') == false) {toggle = true}
     });
     labels.each(function () {
     $(this).toggleClass('is-checked', toggle);
     });

     //console.log(target.parents('ul'))
     },
     */
});

var fadeTime = 100;

function hideEverything() {
    $('.topics_list').fadeOut(fadeTime);
    $('.sources_list').fadeOut(fadeTime);
    $('.return_to_topics').fadeOut(fadeTime);
    $('.titles .mdl-grid').fadeOut(fadeTime);
    $('.add_source_form').fadeOut(fadeTime);
}

function switchTo(section, hide = true) {
    if (hide) hideEverything();
    else $('.titles .mdl-grid').fadeOut(20);
    setTimeout(function () {
        switch(section) {
            case 'sources':
                $('.sources_list').fadeIn(fadeTime);
                $('.return_to_topics').fadeIn(fadeTime);
                $('.add_source_form').fadeIn(fadeTime);
                break;
            case 'topics':
                $('.topics_list').fadeIn(fadeTime);
                break;
            case 'titles':
                //$('.titles .mdl-grid').fadeIn(fadeTime);
                var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
                if (width > 1000) {
                    var stickyHeaderTop = $('.titles').offset().top;
                    $(window).scroll(function(){
                        if( $(window).scrollTop() > stickyHeaderTop ) {
                            $('.titles').css('max-width', $('.titles').css('width'));
                            $('.titles').css({position: 'fixed', top: '0px'});
                            //$('#sticky').css('display', 'block');
                        } else {

                            $('.titles').css({position: 'static', top: '0px'});
                            //$('#sticky').css('display', 'none');
                        }
                    });
                }
        }
    }, fadeTime);
}

