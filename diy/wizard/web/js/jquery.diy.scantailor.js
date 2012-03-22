/* diy ebook creator jquery */

var int;
function progress() {
	$.getJSON('/batch-cmd-get-progress/', function(data) {
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
				$('#progressbar-details').html('Step ' + Number(data.fields.k) + ' / ' + Number(data.fields.v) + ' ( ' + percent + '% ) ' + '<br/><br/>' + data.fields.p + '</p>')
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
	
	$("#start-processing").click(function(event) {
		event.preventDefault();
		$("#dialog-progress").dialog('open');
		$.getJSON("/batch-cmd/",{},function(data) {},"html")
		int=self.setInterval("progress()",500);		
	});
	
	$("#dialog-confirm" ).dialog({
			autoOpen: false,
			resizable: true,
			height:340,
			width:460,
			modal: true,
			buttons: {
				"Yes": function() {
					$( this ).dialog( "close" );
					$.get(
							"/batch-cmd/",
							{ key: "value" },
							function(data) { $('#step3-directory').val((data)); },
							"html"
						);
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
				$.getJSON("/batch-cmd-cancel/",{});
				$( this ).dialog( "close" );
				clearInterval(int)
			}
		}
	});
})
