jQuery.fn.center = function (container) {
	var container = container || $(window);

    this.css("position","absolute");
    this.css("top", Math.max(0, ((container.height() - this.outerHeight()) / 2) + 
                                                container.scrollTop()) + "px");
    this.css("left", Math.max(0, ((container.width() - this.outerWidth()) / 2) + 
                                                container.scrollLeft()) + "px");
    return this;
}