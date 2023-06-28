/********************************************************************************

	SYNCER 〜 知識、感動をみんなと同期(Sync)するブログ

	* 配布場所
	https://syncer.jp/how-to-make-smooth-scroll-without-jquery

	* 最終更新日時
	2015/10/25 15:57

	* 作者
	あらゆ

	** 連絡先
	Twitter: https://twitter.com/arayutw
	Facebook: https://www.facebook.com/arayutw
	Google+: https://plus.google.com/114918692417332410369/
	E-mail: info@syncer.jp

	※ バグ、不具合の報告、提案、ご要望など、お待ちしております。
	※ 申し訳ありませんが、ご利用者様、個々の環境における問題はサポートしていません。

********************************************************************************/


/**************************************************

	smooth-scrollを起動する

**************************************************/
smoothScroll.init({
	selector: '[data-scroll]',						// スムーススクロールが有効なリンクに付ける属性
	selectorHeader: '[data-scroll-header]',			// 固定ナビに付ける属性
	speed: 5000,										// 到達するまでの総時間(ミリ秒)
	easing: 'easeInOutCubic',						// スピードの種類
	offset: 0,										// 到達場所からズラすピクセル数
	updateURL: false,								// URLを[#〜]に変更するか？
	callback: function () {}						// コールバック関数 (到達時に実行される関数)
}) ;
