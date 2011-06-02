/* broken jquery port */

var url = '/ratings/submit';
var leftMargin  = 0;    // The width in pixels of the margin before the stars. */
var starWidth   = 17;   // The width in pixels of each star. */
var starMargin  = 4;    // The width in pixels between each star. */
var scale       = 5;    // It's a five-star scale. */
var snap        = 1;    // Will snap to the nearest star (can be made a decimal, too). */
var activeColor = activeColor;
var votedColor  = votedColor;
var fillColor   = fillColor;

fillVote = function(percent, fill) {
    newFill = getFillPercent(percent);
	if (getVotePercent(newFill) > 100) { newFill = getFillPercent(100) };
    fill.css('width', newFill);
}
getStarPercent = function(id) {
	var stars = id.match(/([^-]+)-(\d*\.?\d+)_(\d*\.?\d+)$/);
    var ratableId = stars[1];
	var score = stars[2];
	var scale = stars[3];
	var percent =  (score / scale) * 100;
	return percent;
}
getFillPercent = function (starPercent) {
	return (starPercent/100)*((starWidth+starMargin)*scale) + leftMargin;
}
getVotePercent = function(divPosition) {
	var starsWidth = (starWidth+starMargin)*scale;
	var offset = leftMargin;
	var starPosition = divPosition - leftMargin;
	var percent = (starPosition / starsWidth * 100);
	return percent;
}
getRatableId= function(id) {
	var stars = id.match(/([^-]+)-(\d*\.?\d+)_(\d*\.?\d+)$/);
	return stars[1];
}
$(document).ready(function() {
  $('.Rating').each(function() {
    id = $(this).attr("id");
    wrapper = $(this).find('.wrapper');
	textEl = $(this).find('.ratingText');
	offset = $(this).position().left;
	fill = $(this).find('.ratingFill');
	starPercent = getStarPercent(id);
	ratableId = getRatableId(id);
	fillVote(starPercent, fill);
	currentFill = getFillPercent(starPercent);
    mouseCrap = function(e) {
        var currentFill = e.pageX - offset;
		var fillPercent = getVotePercent(currentFill);
		var step = (100 / scale) * snap;
		var nextStep = Math.floor(fillPercent / step) + 1;
		fillVote(nextStep * step, fill);
	    //alert(nextStep * step);
    } 
    wrapper.mouseover(function(e) { 
        fill.switchClass("Rating","ratingActive", 500); 
		fill.mousemove(mouseCrap);
    });
    wrapper.mouseleave(function(e) {
		fill.removeClass('ratingActive');
	    fill.unbind('mouseover');
        fill.switchClass("Rating","ratingFill", 500);
	    fillVote(starPercent, fill);
    });
    /*
    wrapper.mousedown(function(e) {
        currentFill = newFill
        fill.switchClass("Rating", "ratingVoted", 500);
		fill.addClass('ratingVoted');
		textEl.addClass('loading');
		var votePercent = getVotePercent(newFill);
		if (url != null) {
            $.post(url,{vote: votePercent,id: ratableId}, updateText("Thanks for voting!"));
		}
	});
    updateText = function(text) {
		error = text.split('ERROR:')[1];
		textEl.removeClass('loading');
		if (error) { el.showError(error); return false; }
		textEl.html(text);
	};
    /*
    showError = function(error) {
		textEl.addClass('ratingError');
		oldTxt = textEl.get('text');
		textEl.set('text', error);
		(function() {
			textEl.set('text', oldTxt);
			textEl.removeClass('ratingError');
		}).delay(1000);
	};
    */
  });
}); 
