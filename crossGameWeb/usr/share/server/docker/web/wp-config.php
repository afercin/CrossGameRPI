<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'root' );

/** MySQL database password */
define( 'DB_PASSWORD', 'patata123' );

/** MySQL hostname */
define( 'DB_HOST', '192.168.1.4' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'li`e@biA8+1NdBnc<(7uoAy7-qlBz!KIPJuX#o^j#bH;rV^$?.yl%MgFa_{P]56y' );
define( 'SECURE_AUTH_KEY',  'u=4UUX12;&*s|R-U-}nawO_otNvNLZs]2LJ<u>5O8Xxr.jVYFR4X<K,p*G+vr?&;' );
define( 'LOGGED_IN_KEY',    'q?ZquzhVrDMfHuVOS78+#i_?S,3{cQJ&0&u>Rvu13F/67F)_qy7m1s%$kbds2NU)' );
define( 'NONCE_KEY',        'Dhq)i?W^~MWGf^]t2r+I$>|^M@tYo,dcMwjpBt~-anI7 lHE>i]ev6Z PSqqqrs ' );
define( 'AUTH_SALT',        'u~z7<?N(@g;J/ =#10x>E?]@fYuY5q1A LO4eH7%e />Wh+k-|WYvt+g|~LX@g=s' );
define( 'SECURE_AUTH_SALT', 'p._ES8tXRJ`DxyQ=n~0W@B;!)7 &6E+?;s&;FBn,vcm~k+^{C)?rEhG4.0$K.kBs' );
define( 'LOGGED_IN_SALT',   'bqlAjW*X??6dl^)S^gw&)3{)@7I?~|&]TRzxr=/Wg#W3G{/l)O9P;uiJG9HP^?)k' );
define( 'NONCE_SALT',       'sk$olE}.hCsCx<((!UQMn*?pR#{/|OAkt`}#>nV+`mh]8r#T|%90==8ToDf/- I[' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
