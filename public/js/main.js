function reloadCloud() {
	if (!pause) {
		$.getJSON('/topics', termCloud.refresh);	
	}
}

$("#cloud").center();
var pause = false
var termCloud = new TermCloud("#cloud");
reloadCloud();

setInterval(reloadCloud, 3000);

$(document).bind('keydown', 'p', function() {
	pause = !pause;
});

