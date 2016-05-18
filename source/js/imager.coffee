do ->
  actualResizeHandler = ->
    imageHeight = $('.tabs--content--container.active .people--item--image').width()
    $('.people--item--image').height(imageHeight)
    return
  document.addEventListener 'DOMContentLoaded', ->
    actualResizeHandler()
    return

  window.addEventListener 'resize', _.debounce(actualResizeHandler, 200, {maxWait: 500}), false
  return