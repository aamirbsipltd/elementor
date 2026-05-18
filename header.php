<?php
/**
 * Site header — used by EVERY page (Elementor pages render between this
 * header and footer.php since we switched off `elementor_canvas`).
 *
 * Structure mirrors the Figma reference:
 *   1. Notice bar (purple) — closure notice + top-right links (Contact / Events / Donate / EN)
 *   2. Main header (white) — logo + primary nav + search + DONATE + GET SUPPORT
 */
$logo_uri = get_theme_file_uri( '/assets/img/logo/logo.png' );
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="ciwa-site-header">

	<!-- Notice bar -->
	<div class="ciwa-notice-bar">
		<div class="ciwa-notice-bar__inner">
			<p class="ciwa-notice-bar__text">
				<?php esc_html_e( 'Centre Closure Notice: Our office will be closed on Monday, July 1st for Canada Day. Programs will resume Tuesday.', 'ciwa-elementor' ); ?>
			</p>
			<ul class="ciwa-notice-bar__links">
				<li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Contact Us', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/events/' ) ); ?>"><?php esc_html_e( 'Events', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/donate/' ) ); ?>"><?php esc_html_e( 'Donate', 'ciwa-elementor' ); ?></a></li>
				<li class="ciwa-notice-bar__lang"><a href="#"><?php esc_html_e( 'EN', 'ciwa-elementor' ); ?></a></li>
			</ul>
		</div>
	</div>

	<!-- Main header -->
	<div class="ciwa-main-header">
		<div class="ciwa-main-header__inner">

			<a class="ciwa-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>">
				<?php if ( file_exists( get_template_directory() . '/assets/img/logo/logo.png' ) ) : ?>
					<img src="<?php echo esc_url( $logo_uri ); ?>" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" />
				<?php else : ?>
					<span class="ciwa-logo__text"><?php bloginfo( 'name' ); ?></span>
				<?php endif; ?>
			</a>

			<nav class="ciwa-main-nav" aria-label="<?php esc_attr_e( 'Primary navigation', 'ciwa-elementor' ); ?>">
				<?php
				wp_nav_menu( array(
					'theme_location' => 'primary',
					'menu_class'     => 'ciwa-main-nav__list',
					'container'      => false,
					'fallback_cb'    => 'ciwa_elementor_fallback_menu',
					'depth'          => 2,
				) );
				?>
			</nav>

			<div class="ciwa-main-header__actions">
				<button class="ciwa-main-header__search" aria-label="<?php esc_attr_e( 'Search', 'ciwa-elementor' ); ?>" type="button">
					<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="9" cy="9" r="7" stroke="#6a1753" stroke-width="2"/>
						<path d="M14 14L18 18" stroke="#6a1753" stroke-width="2" stroke-linecap="round"/>
					</svg>
				</button>
				<a class="ciwa-btn ciwa-btn--pink" href="<?php echo esc_url( home_url( '/donate/' ) ); ?>"><?php esc_html_e( 'DONATE', 'ciwa-elementor' ); ?></a>
				<a class="ciwa-btn ciwa-btn--orange" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'GET SUPPORT', 'ciwa-elementor' ); ?></a>
			</div>

		</div>
	</div>

</header>

<main id="primary" class="ciwa-site-main">
