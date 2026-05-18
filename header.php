<?php
/**
 * Minimal header — only used by fallback templates (index, archive, search,
 * 404). All real pages use Elementor Canvas which bypasses this entirely.
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header style="background:var(--ciwa-primary);color:var(--ciwa-primary-fg);padding:16px 24px;">
	<a href="<?php echo esc_url( home_url( '/' ) ); ?>" style="color:#fff;text-decoration:none;font-family:var(--ciwa-display);font-size:1.4rem;letter-spacing:0.04em;text-transform:uppercase;">
		<?php bloginfo( 'name' ); ?>
	</a>
</header>
