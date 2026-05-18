<?php
/**
 * CIWA Elementor — auto-seed 20 blank WordPress Pages on theme activation.
 *
 * Each page is created with Elementor's "Canvas" template assigned via
 * post meta `_wp_page_template`, which means Elementor renders the page
 * fully without the theme's header/footer. Page authors edit via the
 * "Edit with Elementor" button in wp-admin.
 *
 * The seed runs ONCE on theme activation. Subsequent re-activations skip
 * any slug that already exists, so customer edits are never overwritten.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function ciwa_elementor_page_definitions() {
	return array(
		'home'                       => 'Home',
		'who-we-are'                 => 'Who We Are',
		'leadership-governance'      => 'Leadership and Governance',
		'board-of-directors'         => 'Board of Directors',
		'awards-recognition'         => 'Awards and Recognition',
		'annual-reports'             => 'Annual Reports',
		'settlement-supports'        => 'Settlement Supports',
		'employment-skills-training' => 'Employment Skills and Training',
		'family-parenting-supports'  => 'Family and Parenting Supports',
		'language-training'          => 'Language Training',
		'wellness'                   => 'Wellness Programs',
		'partner-with-us'            => 'Partner With Us',
		'donate'                     => 'Donate',
		'volunteer-with-us'          => 'Volunteer With Us',
		'become-a-member'            => 'Become a Member',
		'news'                       => 'News',
		'events'                     => 'Events',
		'newsletter'                 => 'Newsletter',
		'useful-links'               => 'Useful Links',
		'contact'                    => 'Contact',
	);
}

function ciwa_elementor_seed_pages() {
	$home_id = 0;
	foreach ( ciwa_elementor_page_definitions() as $slug => $title ) {
		$existing = get_page_by_path( $slug, OBJECT, 'page' );
		if ( $existing ) {
			if ( 'home' === $slug ) {
				$home_id = (int) $existing->ID;
			}
			continue;
		}

		$post_id = wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_title'   => $title,
			'post_name'    => $slug,
			'post_content' => sprintf(
				'<p>%s — open in <a href="%s">Edit with Elementor</a> to start building.</p>',
				esc_html( $title ),
				admin_url( 'post.php?post=PLACEHOLDER&action=elementor' )
			),
			'post_author'  => 1,
		) );

		if ( $post_id && ! is_wp_error( $post_id ) ) {
			// Assign Elementor Canvas template — bypasses theme header/footer.
			update_post_meta( $post_id, '_wp_page_template', 'elementor_canvas' );
			// Mark page as Elementor-built (Elementor reads this on first edit).
			update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
			update_post_meta( $post_id, '_elementor_template_type', 'wp-page' );
			update_post_meta( $post_id, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );

			if ( 'home' === $slug ) {
				$home_id = (int) $post_id;
			}
		}
	}

	if ( $home_id ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $home_id );
	}

	// Pretty permalinks.
	if ( '/%postname%/' !== get_option( 'permalink_structure' ) ) {
		update_option( 'permalink_structure', '/%postname%/' );
		global $wp_rewrite;
		if ( $wp_rewrite ) {
			$wp_rewrite->set_permalink_structure( '/%postname%/' );
			flush_rewrite_rules( true );
		}
	}
}
add_action( 'after_switch_theme', 'ciwa_elementor_seed_pages' );
