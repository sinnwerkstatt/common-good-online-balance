$("#id_evaluation_type").change(function() {
	var selected = $("#id_evaluation_type").find(":selected").attr('value');
	if (selected == "single") {
		$("#div_id_consultant").show();
		$("#div_id_auditor").show();
		$("#div_id_accompanying_consultant").show();
	}
	else {
		$("#div_id_consultant").hide();
		$("#div_id_auditor").hide();
		$("#div_id_accompanying_consultant").hide();
	}
});

$("#id_evaluation_type").change();