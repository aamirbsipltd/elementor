<?php
/**
 * Site footer — mirrors the Figma reference:
 *
 *   Top section (purple #6a1753): 4-col grid
 *     1. OUR NEWSLETTER  — heading + sub + email input (white) + orange arrow button
 *     2. QUICK LINKS     — text links (About / Programs / Careers / Volunteer / News /
 *                          Contact & Locations / land acknowledgement / Donate Now)
 *     3. CONTACT INFO    — name + Charitable Registration + address + email + phone
 *     4. FOLLOW US       — text social links: Facebook · Instagram · LinkedIn · YouTube
 *
 *   Bottom section: thin separator + copyright LEFT, Privacy | Accessibility | Sitemap RIGHT
 */
?>
</main>

<footer class="ciwa-footer">

	<div class="ciwa-footer__inner">

		<div class="ciwa-footer-newsletter">
			<h4 class="ciwa-footer__h"><?php esc_html_e( 'Our Newsletter', 'ciwa-elementor' ); ?></h4>
			<p><?php esc_html_e( 'Subscribe to our newsletter', 'ciwa-elementor' ); ?></p>
			<form class="ciwa-news-form" method="post" action="#">
				<input type="email" placeholder="<?php esc_attr_e( 'Type your Email Here', 'ciwa-elementor' ); ?>" required />
				<button type="submit" aria-label="<?php esc_attr_e( 'Subscribe', 'ciwa-elementor' ); ?>">&rarr;</button>
			</form>
		</div>

		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer__h"><?php esc_html_e( 'Quick Links', 'ciwa-elementor' ); ?></h4>
			<p><a href="<?php echo esc_url( home_url( '/who-we-are/' ) ); ?>"><?php esc_html_e( 'About CIWA', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/settlement-supports/' ) ); ?>"><?php esc_html_e( 'Programs & Services', 'ciwa-elementor' ); ?></a></p>
			<p><a href="#careers"><?php esc_html_e( 'Careers', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/volunteer-with-us/' ) ); ?>"><?php esc_html_e( 'Volunteer', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/news/' ) ); ?>"><?php esc_html_e( 'News & Events', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Contact & Locations', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/who-we-are/#land' ) ); ?>"><?php esc_html_e( 'land acknowledgement', 'ciwa-elementor' ); ?></a></p>
			<p><a href="<?php echo esc_url( home_url( '/donate/' ) ); ?>"><?php esc_html_e( 'Donate Now', 'ciwa-elementor' ); ?></a></p>
		</div>

		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer__h"><?php esc_html_e( 'Contact Info', 'ciwa-elementor' ); ?></h4>
			<p><?php esc_html_e( "Canadian Immigrant Women's Association", 'ciwa-elementor' ); ?></p>
			<p><?php echo wp_kses_post( 'Charitable Registration # 118823657 RR0001' ); ?></p>
			<p><?php echo wp_kses_post( '#200, 138&ndash;4th Avenue SE, Calgary AB T2G 4Z6' ); ?></p>
			<p><a href="mailto:welcome@ciwa.org">welcome@ciwa.org</a></p>
			<p><a href="tel:+14032634414">403-263-4414</a></p>
		</div>

		<div class="ciwa-footer-col">
			<h4 class="ciwa-footer__h"><?php esc_html_e( 'follow Us', 'ciwa-elementor' ); ?></h4>
			<p>
				<a href="#facebook"><?php esc_html_e( 'Facebook', 'ciwa-elementor' ); ?></a> &middot;
				<a href="#instagram"><?php esc_html_e( 'Instagram', 'ciwa-elementor' ); ?></a> &middot;
				<a href="#linkedin"><?php esc_html_e( 'LinkedIn', 'ciwa-elementor' ); ?></a> &middot;
				<a href="#youtube"><?php esc_html_e( 'YouTube', 'ciwa-elementor' ); ?></a>
			</p>
		</div>

	</div>

	<hr class="ciwa-footer__sep">

	<div class="ciwa-footer__bottom">
		<p>&copy; <?php echo esc_html( date_i18n( 'Y' ) ); ?> <?php esc_html_e( "Canadian Immigrant Women's Association | All Rights Reserved.", 'ciwa-elementor' ); ?></p>
		<p>
			<a href="#privacy"><?php esc_html_e( 'Privacy Policy', 'ciwa-elementor' ); ?></a> |
			<a href="#accessibility"><?php esc_html_e( 'Accessibility', 'ciwa-elementor' ); ?></a> |
			<a href="#sitemap"><?php esc_html_e( 'Sitemap', 'ciwa-elementor' ); ?></a>
		</p>
	</div>

</footer>

<?php wp_footer(); ?>
</body>
</html>
