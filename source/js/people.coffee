document.addEventListener "DOMContentLoaded", ->
  mouseOverListener = ->
    @classList.add('hover')

  mouseOutListener = ->
    @classList.remove('hover')

  touchStartListener = (e) ->
    @dataset["touchX"] = e.touches[0].clientX
    @dataset["touchY"] = e.touches[0].clientY
    @dataset["touchStamp"] = new Date().getTime()

    # This is a touch device, stop listening on mouse events (for devices that have both)
    @removeEventListener('mouseover', mouseOverListener)
    @removeEventListener('mouseout', mouseOutListener)

  touchEndListener = (e) ->
      dx = e.changedTouches[0].clientX - parseFloat(@dataset["touchX"])
      dy = e.changedTouches[0].clientY - parseFloat(@dataset["touchY"])
      dt = new Date().getTime() - parseInt(@dataset["touchStamp"])
      dist = Math.sqrt(dx*dx + dy*dy)

      # Only flip if it's a tap not a drag (i.e. scrolling)
      if dist < 50 && dt < 400
        @classList.toggle('hover')

  for elem in document.getElementsByClassName("people--item--image")
    elem.addEventListener 'touchstart', touchStartListener
    elem.addEventListener 'touchend', touchEndListener
    elem.addEventListener 'mouseover', mouseOverListener
    elem.addEventListener 'mouseout', mouseOutListener
