<?php
/**
 * CIWA Elementor — minimal theme designed to be edited in Elementor.
 *
 * The theme itself does almost nothing — Elementor's Canvas template
 * takes over rendering for every page. This file handles:
 *
 *   1. Theme support flags (post thumbnails, title-tag, HTML5)
 *   2. Frontend stylesheet enqueue (brand CSS tokens only)
 *   3. Self-hosted brand font registration
 *   4. Plugin-install notices (free Elementor + Elementor Pro)
 *   5. Page seeder (20 blank pages on activation, all set to Elementor Canvas)
 *   6. Elementor preset registration (Global Colors / Global Fonts seeded from
 *      the CIWA brand palette so any new widget pulls from brand tokens)
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'ciwa_elementor_setup' ) ) {
	function ciwa_elementor_setup() {
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'title-tag' );
		add_theme_support( 'html5', array( 'search-form', 'comment-form', 'gallery', 'caption' ) );
		add_theme_support( 'automatic-feed-links' );

		register_nav_menus( array(
			'primary' => __( 'Primary Menu', 'ciwa-elementor' ),
			'footer'  => __( 'Footer Menu', 'ciwa-elementor' ),
		) );
	}
}
add_action( 'after_setup_theme', 'ciwa_elementor_setup' );

/** Enqueue brand stylesheet (CSS custom properties only — Elementor styles the rest). */
function ciwa_elementor_enqueue() {
	wp_enqueue_style(
		'ciwa-elementor-style',
		get_stylesheet_uri(),
		array(),
		wp_get_theme()->get( 'Version' )
	);

	// Self-hosted fonts (woff2 in /assets/fonts/). Registered via @font-face below.
	if ( file_exists( get_template_directory() . '/assets/fonts' ) ) {
		wp_add_inline_style( 'ciwa-elementor-style', ciwa_elementor_font_face_css() );
	}
}
add_action( 'wp_enqueue_scripts', 'ciwa_elementor_enqueue' );

function ciwa_elementor_font_face_css() {
	$fonts_uri = get_theme_file_uri( '/assets/fonts' );
	return '
		@font-face {
			font-family: "Cormorant Garamond";
			src: url("' . esc_url( $fonts_uri ) . '/cormorant-garamond-regular.woff2") format("woff2");
			font-weight: 400; font-style: normal; font-display: swap;
		}
		@font-face {
			font-family: "Cormorant Garamond";
			src: url("' . esc_url( $fonts_uri ) . '/cormorant-garamond-700.woff2") format("woff2");
			font-weight: 700; font-style: normal; font-display: swap;
		}
		@font-face {
			font-family: "Inter";
			src: url("' . esc_url( $fonts_uri ) . '/inter-regular.woff2") format("woff2");
			font-weight: 400; font-style: normal; font-display: swap;
		}
		@font-face {
			font-family: "Inter";
			src: url("' . esc_url( $fonts_uri ) . '/inter-600.woff2") format("woff2");
			font-weight: 600; font-style: normal; font-display: swap;
		}
	';
}

/** Show admin notice prompting Elementor install if not present. */
function ciwa_elementor_install_notice() {
	if ( did_action( 'elementor/loaded' ) ) {
		return; // Elementor active — nothing to do.
	}
	if ( ! current_user_can( 'install_plugins' ) ) {
		return;
	}
	?>
	<div class="notice notice-warning">
		<p><strong>CIWA Elementor theme requires the Elementor plugin.</strong></p>
		<p>Install the free Elementor plugin from <a href="<?php echo esc_url( admin_url( 'plugin-install.php?s=elementor&tab=search&type=term' ) ); ?>">Plugins → Add New</a> (search "Elementor"), then upload Elementor Pro via Plugins → Add New → Upload.</p>
	</div>
	<?php
}
add_action( 'admin_notices', 'ciwa_elementor_install_notice' );

require_once get_template_directory() . '/inc/elementor-presets.php';
require_once get_template_directory() . '/inc/seed-pages.php';
