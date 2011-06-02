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

$(document).ready(function() {
  $('.Rating').each(function() {
    el = $(this)
    el.fillVote = function(percent, fill) {
      newFill = el.getFillPercent(percent);
	  if (el.getVotePercent(newFill) > 100) { newFill = el.getFillPercent(100) };
      fill.css('width', newFill);
    }
el.getRatableId=function(id) {
	var stars = id.match(/([^-]+)-(\d*\.?\d+)_(\d*\.?\d+)$/);
	return stars[1];
}
el.getStarPercent = function(id) {
	var stars = id.match(/([^-]+)-(\d*\.?\d+)_(\d*\.?\d+)$/);
    var ratableId = stars[1];
	var score = stars[2];
	var scale = stars[3];
	var percent =  (score / scale) * 100;
	return percent;
}
el.getFillPercent = function (starPercent) {
	return (starPercent/100)*((starWidth+starMargin)*scale) + leftMargin;
}
el.getVotePercent = function(divPosition) {
	var starsWidth = (starWidth+starMargin)*scale;
	var offset = leftMargin;
	var starPosition = divPosition - leftMargin;
	var percent = (starPosition / starsWidth * 100);
	return percent;
}
    el.id = el.attr("id");
    el.wrapper = el.find('.wrapper');
	el.textEl = el.find('.ratingText');
	el.offset = el.position().left;
	el.fill = el.find('.ratingFill');
    el.starPercent = el.getStarPercent(el.id);
	el.ratableId = el.getRatableId(el.id);
	el.fillVote(el.starPercent, el.fill);
	el.currentFill = el.getFillPercent(el.starPercent);
    el.mouseCrap = function(e) {
        el.mouseFill = e.pageX - el.offset;
		el.fillPercent = el.getVotePercent(el.mouseFill);
		el.step = (100 / scale) * snap;
		el.nextStep = Math.floor(el.fillPercent / el.step) + 1;
	    //alert(el.nextStep); //this works but notice
		el.fillVote(el.nextStep * el.step, el.fill);
    } 
    el.wrapper.mouseover(function(e) { 
        el.fill.switchClass("Rating","ratingActive", 500); 
		el.fill.mousemove(el.mouseCrap);
    });
    el.wrapper.mouseleave(function(e) {
		el.fill.removeClass('ratingActive');
	    el.fill.unbind('mouseover');
        el.fill.switchClass("Rating","ratingFill", 500);
	    el.fillVote(el.starPercent, el.fill);
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

  // doooh hrm
  //$('.Rating').each(function() {
   // el = $(this)
   // alert(el.id);
    //fail
  //});
});


// ets do our alerts outside the loop otherwise its a fales positive.
