import { Template } from 'meteor/templating';

import './search_form.html';

Template.search_form.events({
    'keydown #filter': function (event) {
        if (event.which === 13) {
            FlowRouter.go('search', {searchQuery: event.target.value});
        }
    },
    'focusout .filter-form': function () {
        if ($('#filter').val() == "") {
            $('.filter-form').toggleClass('is-focused', false);
        }
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
    }
});