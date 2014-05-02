console.log('company balance Inicator JS');

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


var editorId = 'company-balance-indicator-xx-editor';
CKEDITOR.disableAutoInline = true;
CKEDITOR.inline(editorId, ckeditor_config);

//var inputElement = document.getElementById('ohai');
//var slider = new Ctl(inputElement);

var pointsEl = $("#company-balance-indicator-xx-points")

pointsEl.TouchSpin({
    min: 0,
    max: 90,
    step: 1,
    decimals: 0,
    boostat: 3,
    maxboostedstep: 10
});

pointsEl.on('change', function(e) {
    console.log('new points: ' + e.target.value);
});
