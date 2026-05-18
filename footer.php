<?php
/**
 * Site footer — used by EVERY page.
 *
 * Structure mirrors the Figma reference:
 *   1. Main footer (dark) — 4 columns: Newsletter / Quick Links / Contact Info / Follow Us
 *   2. Bottom bar — copyright + Privacy/Accessibility/Sitemap + EN
 */
$logo_uri = get_theme_file_uri( '/assets/img/logo/logo.png' );
?>
</main>

<footer class="ciwa-site-footer">

	<div class="ciwa-site-footer__inner">

		<!-- Column 1: Logo + Newsletter -->
		<div class="ciwa-footer-col ciwa-footer-col--newsletter">
			<a class="ciwa-footer__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>">
				<?php if ( file_exists( get_template_directory() . '/assets/img/logo/logo.png' ) ) : ?>
					<img src="<?php echo esc_url( $logo_uri ); ?>" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" />
				<?php else : ?>
					<span><?php bloginfo( 'name' ); ?></span>
				<?php endif; ?>
			</a>
			<h4 class="ciwa-footer-col__h"><?php esc_html_e( 'Our Newsletter', 'ciwa-elementor' ); ?></h4>
			<p class="ciwa-footer-col__sub"><?php esc_html_e( 'Subscribe to our newsletter', 'ciwa-elementor' ); ?></p>
			<form class="ciwa-footer-newsletter" action="#" method="post">
				<input type="email" name="email" placeholder="<?php esc_attr_e( 'Type your Email Here', 'ciwa-elementor' ); ?>" required />
				<button type="submit" aria-label="<?php esc_attr_e( 'Subscribe', 'ciwa-elementor' ); ?>">&rsaquo;</button>
			</form>
		</div>

		<!-- Column 2: Quick Links -->
		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer-col__h"><?php esc_html_e( 'Quick Links', 'ciwa-elementor' ); ?></h4>
			<ul>
				<li><a href="<?php echo esc_url( home_url( '/who-we-are/' ) ); ?>"><?php esc_html_e( 'About CIWA', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/settlement-supports/' ) ); ?>"><?php esc_html_e( 'Programs & Services', 'ciwa-elementor' ); ?></a></li>
				<li><a href="#"><?php esc_html_e( 'Careers', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/volunteer-with-us/' ) ); ?>"><?php esc_html_e( 'Volunteer', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/news/' ) ); ?>"><?php esc_html_e( 'News & Events', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Contact & Locations', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/who-we-are/#land' ) ); ?>"><?php esc_html_e( 'Land Acknowledgement', 'ciwa-elementor' ); ?></a></li>
				<li><a href="<?php echo esc_url( home_url( '/donate/' ) ); ?>" class="ciwa-footer-donate"><?php esc_html_e( 'Donate Now', 'ciwa-elementor' ); ?></a></li>
			</ul>
		</div>

		<!-- Column 3: Contact Info -->
		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer-col__h"><?php esc_html_e( 'Contact Info', 'ciwa-elementor' ); ?></h4>
			<address>
				<strong><?php esc_html_e( "Canadian Immigrant Women's Association", 'ciwa-elementor' ); ?></strong><br>
				<?php echo wp_kses_post( '#200, 138&ndash;4th Avenue SE,<br>Calgary AB T2G 4Z6' ); ?>
			</address>
			<p><a href="mailto:welcome@ciwa.org">welcome@ciwa.org</a></p>
			<p><a href="tel:+14032634414">403-263-4414</a></p>
		</div>

		<!-- Column 4: Follow Us -->
		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer-col__h"><?php esc_html_e( 'Follow Us', 'ciwa-elementor' ); ?></h4>
			<ul class="ciwa-footer-social">
				<li><a href="#" aria-label="Facebook">
					<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.51 17.52 2 12 2S2 6.51 2 12.06c0 5 3.66 9.13 8.44 9.88V14.95H7.9v-2.89h2.54V9.85c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.57v1.87h2.78l-.45 2.89h-2.33v6.99C18.34 21.19 22 17.06 22 12.06z"/></svg>
				</a></li>
				<li><a href="#" aria-label="Instagram">
					<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.31-1.46.72-2.13 1.39C1.34 2.69.93 3.36.62 4.15.32 4.91.12 5.79.06 7.06.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.79.72 1.46 1.39 2.13.67.67 1.34 1.08 2.13 1.39.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56.79-.31 1.46-.72 2.13-1.39.67-.67 1.08-1.34 1.39-2.13.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91-.31-.79-.72-1.46-1.39-2.13C21.31 1.34 20.64.93 19.85.62 19.09.32 18.21.12 16.94.06 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 105.84 12 6.16 6.16 0 0012 5.84zm0 10.16A4 4 0 1116 12a4 4 0 01-4 4zm6.41-11.85a1.44 1.44 0 11-1.44-1.44 1.44 1.44 0 011.44 1.44z"/></svg>
				</a></li>
				<li><a href="#" aria-label="LinkedIn">
					<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.95v5.66H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.38-1.85 3.62 0 4.29 2.38 4.29 5.48v6.26zM5.34 7.43a2.07 2.07 0 11-.01-4.13 2.07 2.07 0 010 4.13zm1.78 13.02H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
				</a></li>
			</ul>
			<p class="ciwa-footer-charity">
				<?php esc_html_e( 'Charitable Registration #', 'ciwa-elementor' ); ?><br>
				<strong>118823657 RR0001</strong>
			</p>
		</div>

	</div>

	<div class="ciwa-site-footer__bottom">
		<div class="ciwa-site-footer__bottom-inner">
			<p>&copy; <?php echo esc_html( date_i18n( 'Y' ) ); ?> <?php esc_html_e( "Canadian Immigrant Women's Association | All Rights Reserved.", 'ciwa-elementor' ); ?></p>
			<ul>
				<li><a href="#"><?php esc_html_e( 'Privacy Policy', 'ciwa-elementor' ); ?></a></li>
				<li><a href="#"><?php esc_html_e( 'Accessibility', 'ciwa-elementor' ); ?></a></li>
				<li><a href="#"><?php esc_html_e( 'Sitemap', 'ciwa-elementor' ); ?></a></li>
				<li><a href="#"><?php esc_html_e( 'EN', 'ciwa-elementor' ); ?></a></li>
			</ul>
		</div>
	</div>

</footer>

<?php wp_footer(); ?>
</body>
</html>
