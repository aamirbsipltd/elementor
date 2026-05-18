<?php
/**
 * Page template — wraps Elementor body content with theme header + footer.
 *
 * Elementor filters the_content() to render its _elementor_data tree, so
 * calling the_content() here outputs the full Elementor-built page. We omit
 * the page title (Elementor pages set hide_title=yes) and skip the outer
 * <main> width constraint so Elementor sections can go alignfull.
 */
get_header();

while ( have_posts() ) {
	the_post();
	the_content();
}

get_footer();
