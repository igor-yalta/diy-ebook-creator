/* diy ebook creator jquery */

var int;
function progress() {
	$.getJSON('/batch-cmd-get-progress/', function(data) {
		//console.log(data)
		if (jQuery.isEmptyObject(data)) {
			var percent = 0;
		}
		else {
			console.log(data);
			var percent = Number(data.fields.v);
			var msg     = data.fields.p;

			//$('div.ui-progressbar-value').css({'background-image': 'url(/static/img/pbar-ani.gif)'})
			$("#progressbar").progressbar({value: percent});
			
			if (msg =='message') {
				$('#progressbar-details').html(data.fields.v);
			}
			else {
				var step    = Number(data.fields.k);
				var total   = Number(data.fields.m);
				var before  = data.fields.o3;
				var after   = data.fields.o4;
				
				if (after || before ) {
					var alt_msg = "Currently, preview only works when images are located on the same hard drive (e.g. c:\) as this software.";
					var pbi = '<img width="300" height="441" src="' + before + '" alt="' + alt_msg + '" />' +
							  '<img width="300" height="441" src="' + after + '" alt="' + alt_msg + '" />';
				}
				else
				    var pbi = "";
				
				//var img_url2= data.fileds.o3.replace('tif','jpg')

				$('#progressbar-details').html('Step ' + step + ' / ' + total + ' ( ' + percent + '% ) ' + '<br/><br/>' + msg + '</p>');
				$('#progressbar-images').html(pbi);
			}
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
		int=self.setInterval("progress()",2000);		
	});
	
	$("#dialog-confirm" ).dialog({
			autoOpen: false,
			resizable: true,
			height:340,
			width:660,
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
		width:660,
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
