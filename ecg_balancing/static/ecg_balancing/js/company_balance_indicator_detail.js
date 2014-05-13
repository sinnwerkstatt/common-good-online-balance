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


// set indicator name
$('.js-indicator-page-title-inner').html(indicator.shortcode + ' - ' + indicator.name);


// activate indicator editor
var indicatorShortCodeSlug = indicator.shortcodeSlug;

var indicatorPrefixId = 'company-balance-indicator-'+indicatorShortCodeSlug;
var editorId = indicatorPrefixId+'-editor';
CKEDITOR.disableAutoInline = true;
CKEDITOR.inline(editorId, ckeditor_config);

// activate indicator evaluation
var touchSpinSettings = {
    min: 0,
    max: 100,
    step: 10,
    decimals: 0,
    boostat: 3,
    maxboostedstep: 10
};

if (indicator.shortcodeSlug.indexOf('n') == 0) { // if negative criteria
    touchSpinSettings.min = indicator.points;
    touchSpinSettings.max = 0
}

var pointsEl = $('#'+indicatorPrefixId+'-points');
pointsEl.TouchSpin(touchSpinSettings);
pointsEl.on('change', function(e) {
    console.log('new points: ' + e.target.value);
});


// if not negative criteria
if (indicator.shortcodeSlug.indexOf('n') != 0) {

    $('.subindicator-title').each(function(e) {
        var $this = $(this);
        var position = $this.data('position');
        var title = indicator.shortcode + '.' + position;

        $.each(indicator.table.subindicators, function( index, subindicator ) {
            if (subindicator.position === position+'') {
                $this.html(title + ' - ' + subindicator.title);
            }
        });

    });

    if (typeof indicator.table !== 'undefined') {
        // activate subindicators
        $.each(indicator.table.subindicators, function( index, subindicator ) {
            var subIdPrefix = 'company-balance-indicator-'+indicatorShortCodeSlug+'-'+subindicator.position;
            console.log( index + ": " + subIdPrefix );

            // activate editor
            var editorId = subIdPrefix+'-editor';
            CKEDITOR.disableAutoInline = true;
            CKEDITOR.inline(editorId, ckeditor_config);

            // activate evaluation
            pointsEl = $('#'+subIdPrefix+'-points');
            pointsEl.TouchSpin(touchSpinSettings);
            pointsEl.on('change', function(e) {
                console.log('new points: ' + e.target.value);
            });
        });
    }
}
