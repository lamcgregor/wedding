do ->

  throttle = (type, name, obj) ->
    obj = obj or window
    running = false

    func = ->
      if running
        return
      running = true
      requestAnimationFrame ->
        obj.dispatchEvent new CustomEvent(name)
        running = false
        return
      return

    obj.addEventListener type, func
    return

  ### init - you can init any event ###

  throttle 'resize', 'optimizedResize'
  return
# handle event
window.addEventListener 'optimizedResize', ->
  return
optimizedResize = do ->
  callbacks = []
  running = false
  # fired on resize event

  resize = ->
    if !running
      running = true
      if window.requestAnimationFrame
        window.requestAnimationFrame runCallbacks
      else
        setTimeout runCallbacks, 66
    return

  # run the actual callbacks

  runCallbacks = ->
    callbacks.forEach (callback) ->
      callback()
      return
    running = false
    return

  # adds callback to loop

  addCallback = (callback) ->
    if callback
      callbacks.push callback
    return

  { add: (callback) ->
    if !callbacks.length
      window.addEventListener 'resize', resize
    addCallback callback
    return
 }
# start process
optimizedResize.add ->
  return
do ->

  resizeThrottler = ->
    # ignore resize events as long as an actualResizeHandler execution is in the queue
    if !resizeTimeout
      resizeTimeout = setTimeout((->
        resizeTimeout = null
        actualResizeHandler()
        # The actualResizeHandler will execute at a rate of 15fps
        return
      ), 66)
    return

  window.addEventListener 'resize', resizeThrottler, false
  resizeTimeout = undefined

  actualResizeHandler = ->
    imageHeight = $('.people--item--image').width()
    $('.people--item--image').height(imageHeight)
    $('.people--item--titles.expanded .people--item--details').height(imageHeight);
    return
  document.addEventListener 'DOMContentLoaded', ->
    actualResizeHandler()
    return
  return