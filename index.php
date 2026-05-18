<?php
/**
 * Minimal fallback template. Every page in this theme is set to Elementor
 * Canvas via post meta `_wp_page_template`, so this template is only used
 * for archives, search, and 404s.
 */
get_header();
?>
<main id="primary" class="site-main" style="max-width:1200px;margin:64px auto;padding:0 24px;">
	<?php
	if ( have_posts() ) {
		while ( have_posts() ) {
			the_post();
			?>
			<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
				<header class="entry-header">
					<?php the_title( '<h1 class="entry-title" style="font-family:var(--ciwa-display);font-size:2.5rem;margin-bottom:24px;">', '</h1>' ); ?>
				</header>
				<div class="entry-content"><?php the_content(); ?></div>
			</article>
			<?php
		}
	} else {
		?>
		<h1 style="font-family:var(--ciwa-display);">Nothing found.</h1>
		<p><a href="<?php echo esc_url( home_url( '/' ) ); ?>">&larr; Back to home</a></p>
		<?php
	}
	?>
</main>
<?php
get_footer();
