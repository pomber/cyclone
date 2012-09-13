function TermCloud(selector) {
	var self = this;

	self.selector = selector;
	self.container = d3.select(selector);
	self.$container = $(selector);

	self.width = self.$container.width();
	self.height = self.$container.height();

	self.init = function() {	
		self.svg = self.container.append("svg")
	    	.attr("width", self.width)
	    	.attr("height", self.height);

		self.background = self.svg.append("g");

		self.vis = self.svg.append("g")
			.attr("transform", "translate("+ [self.width/2, self.height/2] +")");

		self.layout = d3.layout.cloud()
			.size([self.width, self.height])
			.rotate(function() { return ~~(Math.random() * 5) * 30 - 60; })
			.font("Impact")
			.fontSize(function(d) { return Math.round(10 + d.weight * 80); })
			.on("end", function (terms) { self.redraw(terms); })
			.start();	
		
		self.fill = d3.scale.category20b();
	};

	self.refresh = function(terms) {
		self.layout.stop().words(terms).start();
	};

	self.redraw = function (terms) {
		var transitionDelay = 800;
	  	
	  	var text = self.vis.selectAll("text")
			.data(terms, function(d) { return d.text.toLowerCase(); });
		
		text.transition()
	      .duration(transitionDelay)
	      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
	      .style("font-size", function(d) { return d.size + "px"; });
	      
		text.enter().append("text")
			.attr("text-anchor", "middle")
			.attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
			.style("font-size", function(d) { return d.size + "px"; })
			.on("click", function(d) {
				window.open("https://twitter.com/#!/search/" + d.text, "_blank");
			})
			.style("opacity", 1e-6)
			.transition()
			.duration(transitionDelay)
			.style("opacity", 1);
		
		text.style("font-family", function(d) { return d.font; })
			.style("fill", function(d) { return self.fill(d.text.toLowerCase()); })
			.style("cursor", "pointer")
			.text(function(d) { return d.text; });
		
		var exitGroup = self.background.append("g")
			.attr("transform", self.vis.attr("transform"));

		var exitGroupNode = exitGroup.node();
		text.exit().each(function() {
			exitGroupNode.appendChild(this);
		});

		exitGroup.transition()
			.duration(transitionDelay)
			.style("opacity", 1e-6)
			.remove();
		
		self.vis.transition()
			.delay(transitionDelay)
			.duration(600)
			//TODO scale se deberia borrar
			.attr("transform", "translate(" + [self.width/2, self.height/2] + ")scale(" + 1 + ")");
		};

	self.init();
};