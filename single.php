<?php
/** Blog post fallback — Elementor handles real pages. */
get_header();
?>
<main style="max-width:880px;margin:64px auto;padding:0 24px;">
	<?php
	while ( have_posts() ) {
		the_post();
		the_title( '<h1 style="font-family:var(--ciwa-display);font-size:2.5rem;margin-bottom:8px;">', '</h1>' );
		echo '<p style="color:var(--ciwa-text-muted);font-size:0.9rem;">' . esc_html( get_the_date() ) . '</p>';
		echo '<div class="entry-content">';
		the_content();
		echo '</div>';
	}
	?>
</main>
<?php
get_footer();
