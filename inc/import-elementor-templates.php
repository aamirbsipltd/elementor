<?php
/**
 * CIWA Elementor — auto-import Elementor JSON page templates into the
 * matching seeded WP pages on theme activation.
 *
 * Looks for JSON files at /templates/elementor/<slug>.json — each is an
 * Elementor template export (the same format as Elementor → Templates →
 * Saved → Export). On theme activation, the seeded page with matching slug
 * gets its _elementor_data populated and is flagged for Elementor edit mode.
 *
 * Re-runs on every theme version bump to roll out new layouts.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Map of WP page slug → template JSON filename (relative to /templates/elementor/).
 * Add a row here when a new page template ships in templates/elementor/.
 */
function ciwa_elementor_template_map() {
	return array(
		'partner-with-us' => 'partner-with-us.json',
		// 'home' => 'home.json',
		// 'who-we-are' => 'who-we-are.json',
		// ... etc as templates are built
	);
}

/**
 * Replace placeholder tokens in template JSON with runtime values.
 * - {ASSETS} → absolute URL to the theme's /assets/img directory
 *   (so image widgets resolve correctly regardless of WP base URL).
 */
function ciwa_elementor_resolve_placeholders( $json_string ) {
	$assets_uri = get_theme_file_uri( '/assets/img' );
	return str_replace( '{ASSETS}', $assets_uri, $json_string );
}

/**
 * Import one template into the page matching $slug.
 */
function ciwa_elementor_import_template( $slug, $filename ) {
	$page = get_page_by_path( $slug, OBJECT, 'page' );
	if ( ! $page ) {
		return false;
	}
	$path = get_template_directory() . '/templates/elementor/' . $filename;
	if ( ! file_exists( $path ) ) {
		return false;
	}
	$raw = file_get_contents( $path );
	if ( ! $raw ) {
		return false;
	}
	$raw = ciwa_elementor_resolve_placeholders( $raw );
	$tpl = json_decode( $raw, true );
	if ( ! is_array( $tpl ) || empty( $tpl['content'] ) ) {
		return false;
	}

	// Store as _elementor_data (slash-escaped, Elementor convention).
	$content_json = wp_slash( wp_json_encode( $tpl['content'] ) );
	update_post_meta( $page->ID, '_elementor_data', $content_json );
	update_post_meta( $page->ID, '_elementor_edit_mode', 'builder' );
	update_post_meta( $page->ID, '_elementor_template_type', 'wp-page' );
	update_post_meta( $page->ID, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );

	// Apply page-level settings (e.g., hide_title).
	if ( ! empty( $tpl['page_settings'] ) ) {
		update_post_meta( $page->ID, '_elementor_page_settings', $tpl['page_settings'] );
	}

	// Force the page to use Elementor Canvas template (no theme header/footer).
	update_post_meta( $page->ID, '_wp_page_template', 'elementor_canvas' );

	// Mark this template as imported at the current theme version.
	update_post_meta( $page->ID, '_ciwa_template_version', wp_get_theme()->get( 'Version' ) );

	return true;
}

/**
 * Re-import all mapped templates whenever the theme version bumps.
 * Only marks the version as imported when at least one template succeeded —
 * otherwise the version-check would short-circuit on subsequent runs after
 * a failed first attempt (e.g., when the seeded page hadn't been committed
 * yet during `after_switch_theme` due to lookup caching).
 */
function ciwa_elementor_maybe_import_templates() {
	$current = wp_get_theme()->get( 'Version' );
	$stored  = get_option( 'ciwa_elementor_templates_version', '0' );
	if ( version_compare( $stored, $current, '>=' ) ) {
		return;
	}
	$any_ok = false;
	foreach ( ciwa_elementor_template_map() as $slug => $filename ) {
		// Defeat get_page_by_path cache, in case the seed just committed it.
		clean_post_cache( 0 );
		if ( ciwa_elementor_import_template( $slug, $filename ) ) {
			$any_ok = true;
		}
	}
	if ( $any_ok ) {
		update_option( 'ciwa_elementor_templates_version', $current );
	}
}
add_action( 'init', 'ciwa_elementor_maybe_import_templates' );

/**
 * Also run on first theme activation (in case `init` hasn't fired yet
 * during activation flow).
 */
add_action( 'after_switch_theme', 'ciwa_elementor_maybe_import_templates' );

/**
 * Admin-only diagnostic endpoint.
 *
 *   /wp-admin/?ciwa_diag=1   — dump partner-with-us postmeta state as JSON
 *   /wp-admin/?ciwa_reimport=1 — force re-run of template import (ignores version check)
 *
 * Both require an authenticated admin (manage_options capability).
 */
function ciwa_elementor_handle_diag() {
	if ( ! is_admin() || ! current_user_can( 'manage_options' ) ) {
		return;
	}
	if ( isset( $_GET['ciwa_reimport'] ) ) {
		delete_option( 'ciwa_elementor_templates_version' );
		ciwa_elementor_maybe_import_templates();
		wp_send_json( array(
			'status'  => 'reimported',
			'version' => get_option( 'ciwa_elementor_templates_version' ),
			'map'     => ciwa_elementor_template_map(),
		) );
	}
	if ( isset( $_GET['ciwa_diag'] ) ) {
		$slug = sanitize_text_field( $_GET['ciwa_diag'] ?: 'partner-with-us' );
		$page = get_page_by_path( $slug, OBJECT, 'page' );
		if ( ! $page ) {
			wp_send_json( array( 'error' => 'page not found', 'slug' => $slug ) );
		}
		$meta = get_post_meta( $page->ID );
		$out = array(
			'slug'              => $slug,
			'id'                => $page->ID,
			'title'             => $page->post_title,
			'content_excerpt'   => mb_substr( strip_tags( $page->post_content ), 0, 200 ),
			'has_elementor_data'    => ! empty( $meta['_elementor_data'][0] ),
			'elementor_data_len'    => isset( $meta['_elementor_data'][0] ) ? strlen( $meta['_elementor_data'][0] ) : 0,
			'elementor_data_sample' => isset( $meta['_elementor_data'][0] ) ? mb_substr( $meta['_elementor_data'][0], 0, 250 ) : null,
			'edit_mode'             => $meta['_elementor_edit_mode'][0] ?? null,
			'page_template'         => $meta['_wp_page_template'][0] ?? null,
			'elementor_version'     => $meta['_elementor_version'][0] ?? null,
			'ciwa_template_version' => $meta['_ciwa_template_version'][0] ?? null,
			'options'               => array(
				'ciwa_elementor_templates_version' => get_option( 'ciwa_elementor_templates_version' ),
				'ciwa_elementor_kit_seeded'        => get_option( 'ciwa_elementor_kit_seeded' ),
			),
			'theme_version'         => wp_get_theme()->get( 'Version' ),
			'template_file_exists'  => file_exists( get_template_directory() . '/templates/elementor/' . ( ciwa_elementor_template_map()[$slug] ?? '' ) ),
		);
		wp_send_json( $out );
	}
}
add_action( 'admin_init', 'ciwa_elementor_handle_diag' );
