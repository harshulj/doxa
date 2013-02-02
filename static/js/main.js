$(document).ready(function(){
	$(".dropdown-toggle").click(function(){
		var x = $(this).attr("id");
		if(x==1){
			$(".submenu").hide();
			$(this).attr("id", "0");
		}
		else{
			$(".submenu").show();
			$(this).attr("id", "1");
		}
		return false;
	});
	
	// If mouse clicks on submenu
	$(".dropdown-toggle").mouseup(function(){
		return false
	});

	// If mouse is clicked on document
	$(document).mouseup(function(){
		$(".submenu").hide();
		$(".dropdown-toggle").attr("id", "");
	});
});
