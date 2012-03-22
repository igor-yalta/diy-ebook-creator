/* diy ebook creator jquery */

$(document).ready(function(){
	for (var i = 1; i < 20; i++)
        window.clearInterval(i);

	$("#jqueryNext").click(function(event) {
		event.preventDefault();
		$("#dialog-confirm").dialog('open');
	});
	
	$("#dialog-confirm" ).dialog({
			autoOpen: false,
			resizable: true,
			height:340,
			width:460,
			modal: true,
			buttons: {
				"Yes, these are correct": function() {
					$( this ).dialog( "close" );
					$('#jqueryForm').submit();
				},
				'Cancel': function() {
					$( this ).dialog( "close" );
				}
			}
		});
})
