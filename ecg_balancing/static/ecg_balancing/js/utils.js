'use strict';

var Utils = {};

/**
 * Returns the sum of all integers in the given array.
 *
 * @param intArray the array contain integers of type number and string.
 * @returns {number} the sum of all integers in the array.
 */
Utils.sumIntegersInArray = function (intArray) {

    var sum = 0;
    var arrayLength = intArray.length;
    for (var arrayIndex = 0; arrayIndex < arrayLength; arrayIndex++) {
        sum += parseInt(intArray[arrayIndex], 10);
    }
    return sum;
};

Utils.applyEqualHeightOnResize = function () {
    var currentResizeWidth = $(window).width();
    console.log('applyEqualHeight On Resize');

    // fix for Chrome issue: http://code.google.com/p/chromium/issues/detail?id=133869
    if (currentResizeWidth !== Utils.lastResizeWidth) {
        Utils.lastResizeWidth = currentResizeWidth;
        Utils.applyEqualHeightRecalculate();
    }
};

Utils.applyEqualHeightRecalculate = function () {
//    console.log('Recalculate ...');

    // set height to auto (default) to calculate it again
    Utils.getJsEqualHeightElements().each(function() { // for each element
        $(this).children().each(function () {
            $(this).css({ height: 'auto' });
        });
    });

    // set the max height to all elements
    Utils.applyEqualHeight();
};

Utils.applyEqualHeight = function () {
//    console.log('!!!applyEqualHeight');

    Utils.getJsEqualHeightElements().each(function() { // for each element
        var maxHeight = 0;
        $(this).children().each(function () {
            var curCell = $(this);
            if (curCell.outerHeight() > maxHeight) { // compare heights
                maxHeight = curCell.outerHeight();
//                console.log('maxHeight = ' + maxHeight);
            }
        });
        if (maxHeight !== 0) {
            $(this).children().each(function () {
                $(this).css({ height: maxHeight + 'px' });
            });
        }
    });
};

Utils.getJsEqualHeightElements = function () {
    if (Utils.jsEqualHeightElements === undefined) {
        Utils.jsEqualHeightElements = $('.js-equal-height');
    }
    return Utils.jsEqualHeightElements;
};
