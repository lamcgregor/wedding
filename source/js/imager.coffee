do ->
  actualResizeHandler = ->
    imageHeight = $('.people--item--image').width()
    $('.people--item--image').height(imageHeight)
    $('.people--item--titles.expanded .people--item--details').height(imageHeight);
    return
  document.addEventListener 'DOMContentLoaded', ->
    actualResizeHandler()
    return

  window.addEventListener 'resize', _.debounce(actualResizeHandler, 200, {maxWait: 500}), false
  return