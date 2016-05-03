$(document).ready ->
    console.log("tabs!");
    $tabs = $('.tabs');
    console.log("$tabs", $tabs)
    if $tabs.length > 0
        $(document).on 'click', '.tabs--nav--tab', (e) ->
            console.log("tabs click!")
            e.preventDefault()
            $this = $(this)
            $tabs = $('.tabs--nav--tab')
            $tabs.removeClass('active')
            $this.addClass('active')
            index = $this.index()
            $tabsContents = $('.tabs--content--container')
            $tabsContents.hide()
            $tabsContents.eq(index).show()
