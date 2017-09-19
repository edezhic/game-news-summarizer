import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';
import { hide_dialogs } from './dialog'

Meteor.subscribe('briefs');

import './body.html';
import './side-nav/brief';
import './summaries-grid/summary';
import './dialog';
import './help/help-dialogs'
import './side-nav/side-nav';
import './header/top-menu'
import './header/search_form'
import './summaries-grid/summaries-grid'
import './edit-brief-form/edit-brief-form'
import './stats/stats_form'

Template.registerHelper("isAdmin", function() {
    if (Meteor.user()){
        return Meteor.user().username == 'kennivich';
    }
    return false;
});


Template.body_layout.helpers({
    templateGestures: {
        'swiperight .mdl-layout': function (event, templateInstance) {
            var endPoint = event.pointers[0].pageX;
            var distance = event.distance;
            var origin = endPoint - distance;
            if (origin <= 60 && !$('#side-nav').hasClass('is-visible')) {
                toggle_side_nav('open')
            }
        },
        'swipeleft #side-nav': function (event) {
            toggle_side_nav('close')
        }
    }
});

Template.body_layout.events({
    'click .mdl-layout': function (event) {
        var target = $( event.target );
        if ( !target.is( ".material-icons") && !target.is( "#nav-button" ) && !target.is( ".active-element" )) {
            toggle_side_nav('close');
            $('.mdl-menu__container').toggleClass('is-visible', false);
            //hide_dialogs();
        }
    },
    'mouseenter .with-tooltip': function (event) {
        var target = $(event.target);
        var id = target.attr('id');
        set_tooltip_css(event, id);

    },
    'mouseleave .with-tooltip': function (event) {
        var target = $(event.target);
        var id = target.attr('id');
        $('.mdl-tooltip[for=' + id + ']').toggleClass('is-active', false);
    },
    'focusin .mdl-textfield': function (event) {
        event.preventDefault();
        var input = $(event.target);
        var mdl_div = $(input).parents('.mdl-textfield');
        mdl_div.toggleClass('is-focused', true);
        mdl_div.toggleClass('is-dirty', false);
    },
    'focusout .mdl-textfield': function () {
        var input = $(event.target);
        var mdl_div = $(input).parent();
        var val = $(input).val();
        event.preventDefault();
        event.stopPropagation();
        mdl_div.toggleClass('is-focused', false);
        mdl_div.toggleClass('is-dirty', val != '');
    },
    'click #close-dialog': function () {
        hide_dialogs();
    }
});

export function set_dialog_action(action) {
    $('.sign-up-dialog #action-button').attr('action', action);
    $('.sign-up-dialog input').val('');
    $('.sign-up-dialog .mdl-textfield').toggleClass('is-invalid', false);
    $('.sign-up-dialog .mdl-textfield').toggleClass('is-dirty', false);


    const new_brief_button = "<button id='new-brief-button' class='mdl-button mdl-js-button mdl-button--icon mdl-color-text--pink-500 with-tooltip'><i class='material-icons'>add</i></button><div class='mdl-tooltip' for='new-brief-button'>Create Brief</div>"
    const login_button = "<button type='button' class='mdl-button mdl-js-button mdl-button--icon with-tooltip mdl-color-text--pink-500' id='login'><i class='material-icons'>exit_to_app</i></button><div class='mdl-tooltip' for='login'>Log in</div>"

    if (action == 'New') {
        $('.sign-up-dialog .action').html("New Brief");
        $('.sign-up-dialog .button').html(login_button);
        $('.sign-up-dialog #action-button').html('Create');
    }

    if (action == 'Log in') {
        $('.sign-up-dialog .action').html("Log in");
        $('.sign-up-dialog .button').html(new_brief_button);
        $('.sign-up-dialog #action-button').html('Log in');

    }
    dialog = document.querySelector('.sign-up-dialog');
    if (!dialog.open) {dialog.showModal()}

    toggle_side_nav('close');
}


function set_tooltip_css(event, id) {
    var tooltip = $('.mdl-tooltip[for=' + id + ']')[0];
    if (!tooltip) return;
    var props = event.target.getBoundingClientRect();
    var left = props.left + (props.width / 2);
    var top = props.top + (props.height / 2);
    var marginLeft = -1 * (tooltip.offsetWidth / 2);
    var marginTop = -1 * (tooltip.offsetHeight / 2);

    var CssClasses_ = {
        IS_ACTIVE: 'is-active',
        BOTTOM: 'mdl-tooltip--bottom',
        LEFT: 'mdl-tooltip--left',
        RIGHT: 'mdl-tooltip--right',
        TOP: 'mdl-tooltip--top'
    };

    if (tooltip.classList.contains(CssClasses_.LEFT) ||
        tooltip.classList.contains(CssClasses_.RIGHT)) {
        left = (props.width / 2);
        if (top + marginTop < 0) {
            tooltip.style.top = '0';
            tooltip.style.marginTop = '0';
        } else {
            tooltip.style.top = top + 'px';
            tooltip.style.marginTop = marginTop + 'px';
        }
    } else if (left + marginLeft < 0) {
        tooltip.style.left = '0';
        tooltip.style.marginLeft = '0';
    } else {
        tooltip.style.left = left + 'px';
        tooltip.style.marginLeft = marginLeft + 'px';
    }

    if (tooltip.classList.contains(CssClasses_.TOP)) {
        tooltip.style.top =
            props.top - tooltip.offsetHeight - 10 + 'px';
    } else if (tooltip.classList.contains(tooltip.RIGHT)) {
        tooltip.style.left = props.left + props.width + 10 + 'px';
    } else if (tooltip.classList.contains(CssClasses_.LEFT)) {
        tooltip.style.left =
            props.left - tooltip.offsetWidth - 10 + 'px';
    } else {
        tooltip.style.top = props.top + props.height + 10 + 'px';
    }

    tooltip.classList.add('is-active');
}

export function toggle_side_nav(type = '') {
    const side_nav = $('#side-nav');
    if (type == 'close') {
        side_nav.toggleClass('is-visible', false);
        return;
    } else if (type == 'open') {
        side_nav.toggleClass('is-visible', true);
        return;
    }
    side_nav.toggleClass('is-visible');
}

