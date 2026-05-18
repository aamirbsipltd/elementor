<?php
/**
 * CIWA Elementor — seed Elementor's Global Colors + Global Fonts with the
 * CIWA brand tokens, so every widget pulls from brand variables by default
 * instead of hardcoded colors.
 *
 * Runs once on `elementor/loaded` (the first time Elementor boots after
 * the theme is active). Stores a `ciwa_elementor_kit_seeded` option to
 * prevent re-seeding on every page load.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function ciwa_elementor_seed_kit() {
	if ( ! did_action( 'elementor/loaded' ) ) {
		return;
	}
	if ( get_option( 'ciwa_elementor_kit_seeded' ) ) {
		return;
	}

	// Elementor stores Site Settings inside a "kit" post type. Find or create it.
	if ( ! class_exists( '\\Elementor\\Plugin' ) ) {
		return;
	}
	$kit_id = \Elementor\Plugin::$instance->kits_manager->get_active_id();
	if ( ! $kit_id ) {
		return;
	}

	$colors = array(
		array( 'id' => 'primary',      'title' => 'CIWA Primary',     'color' => '#6a1753' ),
		array( 'id' => 'secondary',    'title' => 'CIWA Pink',        'color' => '#e22371' ),
		array( 'id' => 'text',         'title' => 'CIWA Text',        'color' => '#1a1a1a' ),
		array( 'id' => 'accent',       'title' => 'CIWA Orange',      'color' => '#f68b3c' ),
		array( 'id' => 'ciwa-coral',   'title' => 'CIWA Coral',       'color' => '#ff6e6e' ),
		array( 'id' => 'ciwa-teal',    'title' => 'CIWA Teal',        'color' => '#5bbdad' ),
		array( 'id' => 'ciwa-olive',   'title' => 'CIWA Olive',       'color' => '#aaa835' ),
		array( 'id' => 'ciwa-cream',   'title' => 'CIWA Cream',       'color' => '#fdf6ef' ),
		array( 'id' => 'ciwa-pink-bg', 'title' => 'CIWA Pink Surface','color' => '#fce7f0' ),
		array( 'id' => 'ciwa-muted',   'title' => 'CIWA Text Muted',  'color' => '#4a4a4a' ),
		array( 'id' => 'ciwa-border',  'title' => 'CIWA Border',      'color' => '#e6dce4' ),
	);

	$typography = array(
		array(
			'id' => 'primary', 'title' => 'CIWA Display',
			'typography_typography' => 'custom',
			'typography_font_family' => 'Cormorant Garamond',
			'typography_font_weight' => '400',
		),
		array(
			'id' => 'secondary', 'title' => 'CIWA Display Bold',
			'typography_typography' => 'custom',
			'typography_font_family' => 'Cormorant Garamond',
			'typography_font_weight' => '700',
		),
		array(
			'id' => 'text', 'title' => 'CIWA Body',
			'typography_typography' => 'custom',
			'typography_font_family' => 'Inter',
			'typography_font_weight' => '400',
		),
		array(
			'id' => 'accent', 'title' => 'CIWA Body Bold',
			'typography_typography' => 'custom',
			'typography_font_family' => 'Inter',
			'typography_font_weight' => '600',
		),
	);

	$kit_settings = get_post_meta( $kit_id, '_elementor_page_settings', true );
	if ( ! is_array( $kit_settings ) ) {
		$kit_settings = array();
	}
	$kit_settings['system_colors']     = $colors;
	$kit_settings['system_typography'] = $typography;

	// Mark each font/color as custom so Elementor preserves them.
	update_post_meta( $kit_id, '_elementor_page_settings', $kit_settings );

	update_option( 'ciwa_elementor_kit_seeded', 1 );
}
add_action( 'elementor/loaded', 'ciwa_elementor_seed_kit', 20 );
add_action( 'init', 'ciwa_elementor_seed_kit', 99 );
