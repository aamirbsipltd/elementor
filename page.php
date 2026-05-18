<?php
/**
 * Fallback page template — only used if a page doesn't have Elementor
 * Canvas assigned. New pages auto-get Canvas via the seeder.
 */
get_header();
?>
<main style="max-width:1200px;margin:64px auto;padding:0 24px;">
	<?php
	while ( have_posts() ) {
		the_post();
		the_title( '<h1 style="font-family:var(--ciwa-display);font-size:2.5rem;margin-bottom:24px;">', '</h1>' );
		the_content();
	}
	?>
</main>
<?php
get_footer();
