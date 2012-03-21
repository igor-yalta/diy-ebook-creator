/* diy ebook creator jquery */

$.ajaxSetup({ cache: false });

var int;
var temp;
function progress() {
	$.getJSON('/import-cmd-get-progress/', function(data) {
		temp = data;
		console.log(data)
		if (jQuery.isEmptyObject(data)) {
			var percent = 0;
		}
		else {
			console.log(data);
			//$('div.ui-progressbar-value').css({'background-image': 'url(/static/img/pbar-ani.gif)'})
			var percent = Number(data.fields.v);

			$("#progressbar").progressbar({value: percent});
			if (data.fields.p =='message')
				$('#progressbar-details').html(data.fields.v)
			else
				$('#progressbar-details').html(Number(data.fields.k) + ' / ' + Number(data.fields.m) + ' ( ' + percent + '% ) ' + '<br/>' + data.fields.p)
			if (percent == 100) {
				percent = 0
				clearInterval(int)
				$('#progressbar-details').append('<br/> <span class="success"> Complete </span>');
				//$('div.ui-progressbar-value').css({'background-image': 'url()'})
			}
		}
	})
}

function stop_updating() {
	for (var i = 1; i < 10; i++)
	window.clearInterval(i);
}
    
$(document).ready(function(){
	stop_updating();
	
	$("#jqueryNext").click(function(event) {
		event.preventDefault();
		$("#dialog-confirm").dialog('open');
	});
	
	$("#left-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid/",
				{src: $('#step3-directory').val(), card: "left",},
				function(data) {
					if (data.error) {
						alert(data.error + ' Please enter a valid photo folder.');
					}
					else if (data.success) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd/",{src: $('#step3-directory').val(), card: "left",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});
	
	$("#right-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid/",
				{src: $('#step3-directory').val(), card: "right",},
				function(data) {
					if (data.error) {
						alert(data.error + ' Please enter a valid photo folder.');
					}
					else if (data.success) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd/",{src: $('#step3-directory').val(), card: "right",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});
	
	$("#both-card").click(function(event) {
		event.preventDefault();
		$.getJSON("/import-cmd-is-valid/",
				{src: $('#step3-directory').val(), card: "both",},
				function(data) {
					if (data.error) {
						alert(data.error + ' Please enter a valid photo folder.');
					}
					else if (data.success) {
						$("#dialog-progress").dialog('open');
						$.getJSON("/import-cmd/",{src: $('#step3-directory').val(), card: "both",})
					    int=self.setInterval("progress()",100);						
					}
				},
				"html")
	});

	
	$("#step1").click(function(event) {
		$.get(
				"http://localhost/mountpoint",
				{ state: "before" },
				function(data) { $('#step3-directory').val((data)); },
				"html"
			);
	});
	
	$("#step2").click(function(event) {
		$.get(
				"/mountpoint/",
				{ state: "after" },
				function(data) { $('#step3-directory').val((data)); },
				"html"
			);
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
	
	$("#dialog-progress" ).dialog({
		autoOpen: false,
		resizable: true,
		height:440,
		width:560,
		modal: true,
		buttons: {
			"OK": function() {
				$( this ).dialog( "close" );
				clearInterval(int)
			},
			'Cancel': function() {
				stop_updating();
				$.getJSON("/import-cmd-cancel/",{});
				$( this ).dialog( "close" );
				clearInterval(int)
			}
		}
	});
})
