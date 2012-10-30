function reloadCloud() {
	if (!pause) {
		var url = '/topics?p=' + new Date().getTime();
		$.getJSON(url, termCloud.refresh);
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

