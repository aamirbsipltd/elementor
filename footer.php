<?php
/**
 * Minimal footer — only used by fallback templates. Elementor pages bypass.
 */
?>
<footer style="background:#1a1a1a;color:#fff;padding:32px 24px;text-align:center;font-size:0.85rem;margin-top:96px;">
	&copy; <?php echo esc_html( date_i18n( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?>. All rights reserved.
</footer>
<?php wp_footer(); ?>
</body>
</html>
