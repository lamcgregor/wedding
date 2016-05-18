$(document).ready ->
    $tabs = $('.tabs');
    if $tabs.length > 0
        $(document).on 'click', '.tabs--nav--tab', (e) ->
            e.preventDefault()
            $this = $(this)
            $tabs = $('.tabs--nav--tab')
            $tabs.removeClass('active')
            $this.addClass('active')
            index = $this.index()
            $tabsContents = $('.tabs--content--container')
            $tabsContents.removeClass('active')
            $tabsContents.eq(index).addClass('active')
