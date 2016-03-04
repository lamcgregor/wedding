document.addEventListener "DOMContentLoaded", ->
  for elem in document.getElementsByClassName("people--item--image")
    elem.addEventListener 'touchstart', ->
      @classList.toggle('hover')
      @removeEventListener('mouseover')
      @removeEventListener('mouseout')

    elem.addEventListener 'mouseover', ->
      @classList.add('hover')

    elem.addEventListener 'mouseout', ->
      @classList.remove('hover')
