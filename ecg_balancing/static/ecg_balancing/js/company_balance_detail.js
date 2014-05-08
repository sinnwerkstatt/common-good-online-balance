console.log('company balance JS');

Utils.applyEqualHeightRecalculate();

$(".ind-trigger").each(function() {
    var $this = $(this);
    var dataModal = $this.attr("data-modal"); // 'matrix-id'
    var indicatorId = dataModal.substring(7, dataModal.length);

    $this.on('click', function(e) {
        location.href = indicatorBaseUrl + indicatorId;
    });
});
