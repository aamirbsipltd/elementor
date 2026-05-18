<?php
/**
 * Site header — 3 tiers, mirroring the Figma reference:
 *
 *   Tier 1 (pink #e22371)  : closure notice centered, no other links
 *   Tier 2 (cream #fafaf0) : logo LEFT, search bar CENTER, 3 CTAs RIGHT
 *                            (CONTACT US pink-filled / EVENTS orange-outline / DONATE purple-filled)
 *   Tier 3 (purple #6a1753): primary nav LEFT, EN globe RIGHT
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

	<!-- Tier 1: pink notice bar -->
	<div class="ciwa-topbar">
		<p class="ciwa-topbar__text">
			<?php esc_html_e( 'Centre Closure Notice: Our office will be closed on Monday, July 1st for Canada Day. Programs will resume Tuesday.', 'ciwa-elementor' ); ?>
		</p>
	</div>

	<!-- Tier 2: cream — logo + search + CTAs -->
	<div class="ciwa-header-row">
		<div class="ciwa-header-row__inner">

			<a class="ciwa-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php esc_attr_e( 'CIWA — Home', 'ciwa-elementor' ); ?>">
				<?php if ( file_exists( get_template_directory() . '/assets/img/logo/logo.png' ) ) : ?>
					<img src="<?php echo esc_url( $logo_uri ); ?>" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" />
				<?php else : ?>
					<span><?php bloginfo( 'name' ); ?></span>
				<?php endif; ?>
			</a>

			<form class="ciwa-search" role="search" method="get" action="<?php echo esc_url( home_url( '/' ) ); ?>">
				<input type="search" name="s" placeholder="<?php esc_attr_e( 'Search Here', 'ciwa-elementor' ); ?>" aria-label="<?php esc_attr_e( 'Search the site', 'ciwa-elementor' ); ?>" />
				<button type="submit" aria-label="<?php esc_attr_e( 'Search', 'ciwa-elementor' ); ?>">
					<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
						<circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
						<line x1="20" y1="20" x2="16.5" y2="16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
					</svg>
				</button>
			</form>

			<div class="ciwa-header-ctas">
				<a class="ciwa-cta ciwa-cta--pink"   href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'CONTACT US', 'ciwa-elementor' ); ?></a>
				<a class="ciwa-cta ciwa-cta--events" href="<?php echo esc_url( home_url( '/events/' ) ); ?>"><?php esc_html_e( 'EVENTS', 'ciwa-elementor' ); ?></a>
				<a class="ciwa-cta ciwa-cta--purple" href="<?php echo esc_url( home_url( '/donate/' ) ); ?>"><?php esc_html_e( 'DONATE', 'ciwa-elementor' ); ?></a>
			</div>

		</div>
	</div>

	<!-- Tier 3: dark purple — primary nav + EN -->
	<div class="ciwa-navbar">
		<div class="ciwa-navbar__inner">

			<nav class="ciwa-nav" aria-label="<?php esc_attr_e( 'Primary navigation', 'ciwa-elementor' ); ?>">
				<?php
				if ( has_nav_menu( 'primary' ) ) {
					wp_nav_menu( array(
						'theme_location' => 'primary',
						'container'      => false,
						'menu_class'     => '',
						'depth'          => 2,
					) );
				} else {
					ciwa_elementor_fallback_menu();
				}
				?>
			</nav>

			<a class="ciwa-lang" href="#en" aria-label="<?php esc_attr_e( 'Language: English', 'ciwa-elementor' ); ?>">
				<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
					<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
					<path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18" stroke="currentColor" stroke-width="1.6"/>
				</svg>
				<span><?php esc_html_e( 'EN', 'ciwa-elementor' ); ?></span>
			</a>

		</div>
	</div>

</header>

<main id="primary" class="ciwa-site-main">
