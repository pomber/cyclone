function reloadCloud() {
	$.getJSON('/topics', termCloud.refresh);	
}

$("#vis").center();
var termCloud = new TermCloud("#vis");
reloadCloud();

setInterval(reloadCloud, 3000);

