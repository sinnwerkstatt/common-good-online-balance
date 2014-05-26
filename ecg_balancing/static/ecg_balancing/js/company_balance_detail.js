console.log('company balance JS');

Utils.applyEqualHeightRecalculate();

if (is_sole_proprietorship) {
    $('.no-sole-proprietorship').each(function () {
        var $this = $(this);
        $this.removeClass('ind-trigger');
        $this.addClass('active');
    });
}

$(".ind-trigger").each(function () {
    var $this = $(this);
    var dataModal = $this.attr("data-modal"); // 'matrix-id'
    var indicatorId = dataModal.substring(7, dataModal.length);

    var $pointsEl = null;
    var curIndicatorPoints = null;
    $pointsEl = $this.find('.indicator-points');
    if ($pointsEl.length !== 0) {
        // positive indicators
        curIndicatorPoints = indicatorPoints[indicatorId];
        $pointsEl.html(curIndicatorPoints + ' / ' + $pointsEl.html());
    } else {
        $pointsEl = $this.find('.negative-points');
        curIndicatorPoints = indicatorPoints[indicatorId];
        $pointsEl.html(curIndicatorPoints);
    }

    $this.on('click', function (e) {
        location.href = indicatorBaseUrl + indicatorId;
    });

});
