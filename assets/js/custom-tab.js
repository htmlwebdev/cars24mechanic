
    if (jQuery().isotope) {
            window.addEventListener('load', function () {
                // cache container
                var jQuerycontainer1 = jQuery('.our-latest-work-list');
                // initialize isotope
                jQuerycontainer1.isotope({
                    filter: '*',
                    masonry: {
                        columnWidth: 1
                    }
                });
                // filter items when filter link is clicked
                jQuery('#filters a').click(function() {
                    var selector = jQuery(this).attr('data-filter');
                    jQuerycontainer1.isotope({
                        filter: selector
                    });
                    return false;
                });
                // set selected menu items
                var jQueryfilters = jQuery('#filters'),
                    jQueryfiltersLinks = jQueryfilters.find('a');
                    jQueryfiltersLinks.click(function() {
                    console.log(this);
                    var jQuerythis = jQuery(this).parent(this);
                    // don't proceed if already selected
                    if (jQuerythis.hasClass('active')) {
                        return false;
                    }
                    var jQueryfilterLink = jQuerythis.parents('#filters');
                    jQueryfilterLink.find('.active').removeClass('active');
                    jQuerythis.addClass('active');
                });
                var jQuerycontainer2 = jQuery('.gallery');
                // initialize isotope
                jQuerycontainer2.isotope({
                    filter: '*',
                    masonry: {
                        columnWidth: 1,
                        gutterWidth: 0,
                    }
                });
                // filter items when filter link is clicked
                jQuery('#filters a').click(function() {
                    var selector = jQuery(this).attr('data-filter');
                    jQuerycontainer2.isotope({
                        filter: selector
                    });
                    return false;
                });
                // set selected menu items
                var jQueryfilters = jQuery('#filters'),
                    jQueryfiltersLinks = jQueryfilters.find('a');
                jQueryfiltersLinks.click(function() {
                    console.log(this);
                    var jQuerythis = jQuery(this).parent(this);
                    // don't proceed if already selected
                    if (jQuerythis.hasClass('active')) {
                        return false;
                    }
                    var jQueryfilterLink = jQuerythis.parents('#filters');
                    jQueryfilterLink.find('.active').removeClass('active');
                    jQuerythis.addClass('active');
                });
            });
            }