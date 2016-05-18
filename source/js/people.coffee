# Helper for making touch tap listeners
bindTap = (elem, callback) ->
  elem.addEventListener 'touchstart', (e) ->
    @dataset['touchX'] = e.touches[0].clientX
    @dataset['touchY'] = e.touches[0].clientY
    @dataset['touchStamp'] = new Date().getTime()

  elem.addEventListener 'touchend', (e) ->
    dx = e.changedTouches[0].clientX - parseFloat(@dataset['touchX'])
    dy = e.changedTouches[0].clientY - parseFloat(@dataset['touchY'])
    dt = new Date().getTime() - parseInt(@dataset['touchStamp'])
    dist = Math.sqrt(dx*dx + dy*dy)

    # Only flip if it's a tap not a drag (i.e. scrolling)
    if dist < 50 && dt < 400
      callback.apply(this)


document.addEventListener 'DOMContentLoaded', ->
  mouseOverListener = ->
    @classList.add('hover')

  mouseOutListener = ->
    @classList.remove('hover')

  touchStartListener = (e) ->
    # This is a touch device, stop listening on mouse events (for devices that have both)
    @removeEventListener('mouseover', mouseOverListener)
    @removeEventListener('mouseout', mouseOutListener)

  for elem in document.getElementsByClassName('people--item--image')
    elem.addEventListener 'touchstart', touchStartListener
    elem.addEventListener 'mouseover', mouseOverListener
    elem.addEventListener 'mouseout', mouseOutListener

    bindTap elem, ->
      @classList.toggle('hover')


  for elem in document.getElementsByClassName('people--item--titles')
    # Capture timeout variable in a closure
    (->
      collapseTimeout = null
      expandTimeout = null
      titlesElem = elem
      detailsElem = null
      for child in elem.childNodes
        if child.classList?.contains('people--item--details')
          detailsElem = child
      $item = $(detailsElem).parents('.people--item')
      console.log $item.find('.people--item--image').height()
      height = $item.find('.people--item--image').height()
      detailsElem.style.height = 0

      onCollapse = ->
        titlesElem.classList.remove('collapsing')
        detailsElem.style.height = 0

      expandListener = ->
        if @classList.contains('expanded')
          clearTimeout expandTimeout
          collapseTimeout = setTimeout onCollapse, 400

          @classList.remove('expanded')
          @classList.add('collapsing')
          detailsElem.style.height = 0

        else
          clearTimeout collapseTimeout
          height = $item.find('.people--item--image').height()
          detailsElem.style.height = "#{height}px"
          @classList.add('expanded')
          @classList.remove('collapsing')

      bindTap elem, expandListener
      elem.addEventListener 'touchstart', ->
        @removeEventListener 'click', expandListener

      elem.addEventListener 'click', expandListener
    )()


