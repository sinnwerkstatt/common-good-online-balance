// set indicator name
$('.js-indicator-page-title-inner').html(indicator.shortcode + ' - ' + indicator.name);

//$('.save-button-container').affix({
//      offset: {
//        top: $('header').height()
//      }
//});


var is_negative_criteria = indicator.shortcodeSlug.indexOf('n') == 0;

// Add subindicator titles
if (!is_negative_criteria) {

    $('.subindicator-title').each(function (e) {
        var $this = $(this);
        var position = $this.data('position');
        var title = indicator.shortcode + '.' + position;

        $.each(indicator.table.subindicators, function (index, subindicator) {
            if (subindicator.position === position + '' &&
                (!(is_sole_proprietorship && !subindicator.soleProprietorship))) {
                $this.html(title + ' - ' + subindicator.title);
            }
        });
    });
}

// add key figures HTML if existing
// key-figures-container
if (can_edit) {
    $('.key-figures-container').each(function(e) {
        var $keyFiguresContainer = $(this);
        $keyFiguresContainer.addClass('bubble-contents company-balance-indicator-keyfigures');
        if ($keyFiguresContainer.html().trim().length == 0) { // if there is already content, don't add default content
            var indicatorPosition = $keyFiguresContainer.data('indicator-position');
            var indicatorData = null;
            if (typeof indicatorPosition !== 'undefined') {
                indicatorData = indicator.table.subindicators[indicatorPosition-1];
            } else {
                indicatorData = indicator;
            }
            if (typeof indicatorData.keyFigures !== 'undefined') {
                var indicatorSlug = $keyFiguresContainer.data('indicator-slug');
                var keyFiguresHtml = '<textarea name="company-balance-indicator-'+indicatorSlug+'-keyfigures-editor" ' +
                    'id="company-balance-indicator-'+indicatorSlug+'-keyfigures-editor">'
                keyFiguresHtml += indicatorData.keyFigures;
                keyFiguresHtml += '</textarea>';
                $keyFiguresContainer.html(keyFiguresHtml);
            }
        }
    });
}

//if (is_admin) {


var ckeditor_config = {
    // Define changes to default configuration here.
    // For the complete reference:
    // http://docs.ckeditor.com/#!/api/CKEDITOR.config

    language: 'de',
    uiColor: '#F8F8F8',

    // The toolbar groups arrangement, optimized for two toolbar rows.
    toolbar: [
        {
            name: 'basicstyles',
            groups: [ 'basicstyles', 'cleanup' ],
            items: [ 'Bold', 'Italic', 'Underline']
        },
        {
            name: 'colors',
            items: [ 'TextColor', 'BGColor' ]
        },
        {
            name: 'paragraph',
            groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ],
            items: [ 'BulletedList', 'NumberedList', '-', 'Blockquote', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight']
        },
        {
            name: 'links',
            items: [ 'Link', 'Unlink']
        },
        {
            name: 'insert',
            items: [ 'Image', 'Table', 'HorizontalRule']
        },
        {
            name: 'styles',
            items: [ 'Format', 'Font', 'FontSize' ]
        },
        {
            name: 'clipboard',
            groups: [ 'clipboard', 'undo' ],
            items: [ 'Undo', 'Redo' ]
        },
        {
            name: 'tools',
            items: [ 'Maximize']
        },
    ],

    // Toolbar groups configuration.
    toolbarGroups: [
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ] },
        { name: 'forms' },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
        { name: 'links' },
        { name: 'insert' },
        '/',
        { name: 'styles' },
        { name: 'colors' },
        { name: 'tools' },
        { name: 'others' },
        { name: 'about' }
    ],


    // Remove some buttons, provided by the standard plugins, which we don't
    // need to have in the Standard(s) toolbar.
    // config.removeButtons = 'Subscript,Superscript';

    // Se the most common block elements.
    format_tags: 'p;h1;h2;h3;pre',

    // Make dialogs simpler.
    removeDialogTabs: 'image:advanced;link:advanced'

    // plugins
    // extraPlugins : 'onchange',
    // minimumChangeMilliseconds : 200
};

// activate indicator editor
var indicatorShortCodeSlug = indicator.shortcodeSlug;

var indicatorPrefixId = 'company-balance-indicator-' + indicatorShortCodeSlug;
var editorId = indicatorPrefixId + '-editor';
CKEDITOR.disableAutoInline = true;
CKEDITOR.inline(editorId, ckeditor_config);

// activate key figures for the main indicator
var keyfiguresId = indicatorPrefixId + '-keyfigures' + '-editor';
if (document.getElementById(keyfiguresId) !== null) {
    CKEDITOR.disableAutoInline = true;
    CKEDITOR.inline(keyfiguresId, ckeditor_config);
}

// activate indicator evaluation
var touchSpinSettings = {
    min: 0,
    max: 100,
    step: 1,
    decimals: 0,
    boostat: 3,
    maxboostedstep: 10
};

if (indicator.shortcodeSlug.indexOf('n') == 0) { // if negative criteria
    touchSpinSettings.min = indicator.points;
    touchSpinSettings.max = 0;
    touchSpinSettings.step = 10;
}

var pointsEl = $('#' + indicatorPrefixId + '-points');
pointsEl.TouchSpin(touchSpinSettings);
pointsEl.on('change', function (e) {
    console.log('new points: ' + e.target.value);
});

var touchSpinSubindicatorSettings = {
    min: 0,
    max: 100,
    step: 10,
    decimals: 0,
    boostat: 3,
    maxboostedstep: 10
};

// if not negative criteria
if (!is_negative_criteria) {

    if (typeof indicator.table !== 'undefined') {
        // activate subindicators
        $.each(indicator.table.subindicators, function (index, subindicator) {

            // don't active non-SP subindicator for an SP company
            if (!(is_sole_proprietorship && !subindicator.soleProprietorship)) {

                var subIdPrefix = 'company-balance-indicator-' + indicatorShortCodeSlug + '-' + subindicator.position;
                console.log("subindicator " + index + ": " + subIdPrefix);

                // activate editor
                var editorId = subIdPrefix + '-editor';
                CKEDITOR.disableAutoInline = true;
                CKEDITOR.inline(editorId, ckeditor_config);

                // activate key figures
                var keyfiguresId = subIdPrefix + '-keyfigures' + '-editor';
                if (document.getElementById(keyfiguresId) !== null) {
                    CKEDITOR.disableAutoInline = true;
                    CKEDITOR.inline(keyfiguresId, ckeditor_config);
                }

                // activate evaluation
                pointsEl = $('#' + subIdPrefix + '-points');
                pointsEl.TouchSpin(touchSpinSubindicatorSettings);
                pointsEl.on('change', function (e) {
                    console.log('new points: ' + e.target.value);
                });
            }
        });
    }
}

//}
