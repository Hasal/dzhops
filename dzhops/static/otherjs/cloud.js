var _com_favormy_plugin = _com_favormy_plugin || {};

(function(S, undefined) {
    S.Constants = {
        API_SERVER : ('https:' == document.location.protocol ? 'https://' : 'http://') + "fmapi.sinaapp.com/",
        S_SERVER : ('https:' == document.location.protocol ? 'https://' : 'http://') + "favormy.sinaapp.com/",
        GA_ACCOUNT : "UA-28263363-3"
    };
})(_com_favormy_plugin);

var _gaq = _gaq || [];
_gaq.push(['favormy._setAccount', _com_favormy_plugin.Constants.GA_ACCOUNT]);
_gaq.push(['favormy._setAllowLinker', true]);
_gaq.push(['favormy._setDomainName', "auto"]);
_gaq.push(['favormy._setSampleRate', 10]);
_gaq.push(['favormy._setSiteSpeedSampleRate', 10]);
_gaq.push(['favormy._trackPageview']);

(function() {
    var url = document.location.href;
    var regexp = new RegExp("pay\.(360buy|jd)\.com");
    if(!regexp.test(url)) {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    }
})();

(function(S, window, undefined) {
    S.window = window;
    var document = window.document;
    if (document) {
        S.loadJS = function(url, callback) {
            var js = document.createElement('script');
            js.type = 'text/javascript';
            js.async = true;
            js.src = url;
            var s = document.getElementsByTagName('script')[0];

            // Handle Script loading
            var done = false;

            js.onload = js.onreadystatechange = function() {
                if (!done && (!this.readyState || this.readyState === "loaded" || this.readyState === "complete")) {
                    done = true;
                    var endTime = new Date().getTime();
                    var timeSpent = endTime - S.startLoadJSTime[this.src];
                    if (timeSpent >= 0) {
                        _gaq.push([ 'favormy._trackTiming', 'FavorMy', 'Load JS', timeSpent, url ]);
                    }
                    callback();
                    // Handle memory leak in IE
                    js.onload = js.onreadystatechange = null;
                }
            };
            S.startLoadJSTime = S.startLoadJSTime || {};
            S.startLoadJSTime[url] = new Date().getTime();

            s.parentNode.insertBefore(js, s);
        };
        var url = document.location.href;

        var parseUrl = (function () {
            var a = document.createElement('a');
            return function (url) {
                a.href = url;
                return {
                    host: a.host,
                    hostname: a.hostname,
                    pathname: a.pathname,
                    port: a.port,
                    protocol: a.protocol,
                    search: a.search,
                    hash: a.hash
                };
            }
        })();

        var hostname = parseUrl(url).hostname;

        var hosts = [
            "100yue.com",
            "111.com.cn",
            "17ugo.com",
            "189.cn",
            "22shop.com",
            "2688.com",
            "51eshop.com",
            "51sheyuan.com",
            "51xiaoqin.com",
            "51youpin.com",
            "525j.com.cn",
            "525m.com",
            "52xie.com",
            "5lux.com",
            "800pharm.com",
            "818.com",
            "958shop.com",
            "99read.com",
            "9you.com",
            "abesofmaine.com",
            "abs.cn",
            "aidai.com",
            "aigo.com",
            "aigou.com",
            "aimer.com.cn",
            "aircamel.com.tw",
            "aiwuai.com",
            "aizhigu.com.cn",
            "amazon.cn",
            "anngo.net",
            "apple.com",
            "asos.com",
            "babydate.com.cn",
            "baiyjk.com",
            "bangcl.com",
            "banggo.com",
            "beifabook.com",
            "benlai.com",
            "benq.com.cn",
            "bhphotovideo.com",
            "biotherm.com.cn",
            "blemall.com",
            "boee.cn",
            "boheshop.com",
            "bonjourhk.com",
            "bookschina.com",
            "bookuu.com",
            "boots.com",
            "boqii.com",
            "butao.com",
            "buy.com",
            "buynow.com.cn",
            "camel.com.cn",
            "caomeipai.com",
            "carrefour.com.cn",
            "ccb.com",
            "ccbd.cn",
            "ch999.com.cn",
            "chebao360.com",
            "china-pub.com",
            "chinaboke.cn",
            "chinadrtv.com",
            "chinapay.com",
            "clarins.com.cn",
            "clinique.com.cn",
            "cntv.cn",
            "coo8.com",
            "coolpad.cn",
            "cosme-de.com",
            "cqcb.com",
            "d1.com.cn",
            "dada360.com",
            "dakele.com",
            "damai.cn",
            "dangdang.com",
            "daphne.cn",
            "dealtime.com",
            "debenhams.com",
            "detime.com",
            "dhc.net.cn",
            "didamall.com",
            "book.douban.com",
            "doudoutao.com",
            "dsw.com",
            "e-lining.com",
            "eachnet.com",
            "easy361.com",
            "efeihu.com",
            "ehaier.com",
            "ehmall.com.cn",
            "element14.com",
            "enet.com.cn",
            "epetbar.com",
            "esteelauder.com.cn",
            "etam.com.cn",
            "fclub.cn",
            "feifei.com",
            "feiniu.com",
            "fengbuy.com",
            "ffok.cn",
            "freemerce.com",
            "fruitday.com",
            "fuwa.com",
            "gaojie.com",
            "gap.cn",
            "gdcct.com",
            "gewei.com",
            "gg1994.com",
            "giftport.com.cn",
            "gionee.com",
            "giordano.com",
            "gnc.com",
            "gome.com.cn",
            "gongtianxia.com",
            "goodbaby.com",
            "goodjd.com",
            "goujiuwang.com",
            "goumin.com",
            "handu.com",
            "handuyishe.com",
            "hao24.cn",
            "haohaizi.com",
            "happigo.com",
            "hecha.cn",
            "hicdma.com",
            "hisense.com",
            "hitao.com",
            "homevv.com",
            "hp.com",
            "htceshop.com",
            "htexam.com",
            "huatu.com",
            "huihao.com",
            "huihui.cn",
            "hujiang.com",
            "hunhuasuan.com",
            "ibuying.com",
            "ihaveu.com",
            "ihush.com",
            "ikuaigan.com",
            "ilife.cn",
            "ing2ing.com",
            "ingping.com",
            "inoherb.com",
            "inshion.com",
            "is186.com",
            "it007.com",
            "itruelife.com",
            "j1.com",
            "jajn.com",
            "jcang.com.cn",
            "jd.com",
            "360buy.com",
            "jia.com",
            "jiahewh.com",
            "jiaju.com",
            "jiaku.com",
            "jianke.com",
            "jiapin.com",
            "jiatx.com",
            "jimei.com.cn",
            "jingrunshop.com",
            "jiuxian.com",
            "jjlg.com.cn",
            "jpeen.com",
            "jshoppers.com",
            "jufengshang.com",
            "jumei.com",
            "junph.com",
            "justyle.com",
            "jxdyf.com",
            "k-touch.cn",
            "kaicong.net",
            "kangtu.com",
            "kaoyan001.com",
            "keede.com",
            "kela.cn",
            "kongfz.com",
            "korirl.com",
            "kouclo.com",
            "kuaishubao.com",
            "kypbuy.com",
            "ladypk.com",
            "lamiu.com",
            "lancome.com.cn",
            "ledaojia.com",
            "lefeng.com",
            "lenovo.com.cn",
            "lenovomobile.com",
            "letao.com",
            "letv.com",
            "leyou.com.cn",
            "liebo.com",
            "likebuy.com",
            "lingshi.com",
            "liqunshop.com",
            "liwai.com",
            "liwuyou.com",
            "liyi99.com",
            "logitech.com.cn",
            "lorealparis.com.cn",
            "lovo.cn",
            "lusen.com",
            "luxst.com",
            "lvyoumall.com",
            "m18.com",
            "m6go.com",
            "maidezhi.com",
            "maiduo.com",
            "maimaicha.com",
            "masamaso.com",
            "mbaobao.com",
            "meici.com",
            "meilele.com",
            "meiribuy.com",
            "metromall.com.cn",
            "mfhui.com",
            "minitiao.com",
            "miqi.cn",
            "misslele.com",
            "mmall.com",
            "mobi189.com",
            "mogujie.com",
            "momoyoyo.com",
            "monteamor.com",
            "mooiee.com",
            "moonbasa.com",
            "motherbuy.com",
            "moximoxi.net",
            "muyingzhijia.com",
            "mynet.cn",
            "myrainbow.cn",
            "najue.com",
            "nala.com.cn",
            "naruko.com.cn",
            "newegg.cn",
            "nikestore.com.cn",
            "nipponpaint.com.cn",
            "no5.com.cn",
            "obuy.cn",
            "ochirly.com",
            "ocj.com.cn",
            "ofcard.com",
            "okbuy.com",
            "okhqb.com",
            "okjee.com",
            "olomo.com",
            "olympus.com.cn",
            "ono.com.cn",
            "origins.com.cn",
            "osa.com.cn",
            "ouku.com",
            "outlets365.com",
            "overstock.com",
            "oyeah.com.cn",
            "paipai.com",
            "paixie.net",
            "pb89.com",
            "pba.cn",
            "people.com.cn",
            "qinqin.net",
            "qinqinbaby.com",
            "qjherb.com",
            //"qq.com",
            "quwan.com",
            "rayi.cn",
            "redbaby.com.cn",
            "rei.com",
            "rs-online.com",
            "rutisher.com",
            "s.cn",
            "saite.com",
            "samsclub.cn",
            "samsung.com.cn",
            "sanfo.com",
            "sasa.com",
            "sasacity.com",
            "secoo.com",
            "sephora.cn",
            "sfbest.com",
            "shajia.cn",
            "shangpin.com",
            "shishangqiyi.com",
            "shopex.cn",
            "shopin.net",
            "shoubiao.com.cn",
            //"sina.com.cn",
            "sinobuy.cn",
            "sisley.com.cn",
            "sonystyle.com.cn",
            "spider.com.cn",
            "staples.cn",
            "strawberrynet.com",
            "suning.com",
            "suorang.com",
            "t0001.com",
            "tao3c.com",
            "taobao.com",
            "taoshu.com",
            "taoxie.com",
            "tcl.com",
            "teds.com.au",
            "tianpin.com",
            "tiantian.com",
            "time100.cn",
            "tmall.com",
            "tokyopretty.com",
            "tooogooo.com",
            "tootoo.cn",
            "uemall.com",
            "ugou.cn",
            "uiyi.cn",
            "ule.com",
            "un58.com",
            "uniqlo.cn",
            "usashopcn.com",
            "uya100.com",
            "uzise.com",
            "vancl.com",
            "vipshop.com",
            "vjia.com",
            "vmall.com",
            "vsigo.cn",
            "vsnoon.com",
            "wangfujing.com",
            "wanggou.com",
            "wangjiu.com",
            "wansecheng.com",
            "wbiao.cn",
            "wine9.com",
            "winekee.com",
            "winenice.com",
            "winxuan.com",
            "wl.cn",
            "womai.com",
            "wowsai.com",
            "x-kicks.com",
            "x.com.cn",
            "xiangqinyw.com",
            "xiaomi.com",
            "xifuquan.com",
            "xihuojie.com",
            "xijie.com",
            "xinbaigo.com",
            "xiu.com",
            "xmeise.com",
            "xunlei.com",
            "xyb2c.com",
            "xzuan.com",
            "yaahe.cn",
            "yangche51.com",
            "yaofang.cn",
            "yaofangwang.com",
            "yaohongjiu.com",
            "yeecare.com",
            "yesky.com",
            "yesmywine.com",
            "yhd.com",
            "yihaodian.com",
            "yidianda.com",
            "yiguo.com",
            "yintai.com",
            "yixun.com",
            "51buy.com",
            "ymall.com",
            "ymatou.com",
            "yoger.com.cn",
            "yoho.cn",
            "yohobuy.com",
            "yougou.com",
            "youjk.com",
            "youlu.net",
            "yueji.com",
            "yummy77.com",
            "zara.cn",
            "zgshoes.com",
            "zhenpin.com",
            "zhiwo.com",
            "zhuannet.com",
            "zm7.cn",
            "zol.com",
            "zol.com.cn",
            "zte.com.cn",
            "zuipin.cn",
            "zun1.com",
            "zymk.cn"
        ];

        S.pattern = {
            "10000yao.com": {
                "price": [
                    ".box .t2 .each:eq(1)"
                ],
                "name": [
                    ".box .r .title:first"
                ],
                "url": [
                    "^http://www.10000yao.com/product-\\d+.html"
                ]
            },
            "10010.com": {
                "price": [
                    ".goodsPrice:first"
                ],
                "name": [
                    ".goodsName:first"
                ],
                "url": [
                    "^http://www.10010.com/goodsdetail/\\d+.html"
                ]
            },
            "10086.cn": {
                "price": [
                    "#sku_price:first"
                ],
                "name": [
                    ".phone_module h1:first"
                ],
                "url": [
                    "^http://shop.10086.cn/goods/[_0-9]+.html"
                ]
            },
            "amazon.cn": {
                "price": [
                    "#priceblock_dealprice",
                    "#actualPriceValue>.priceLarge",
                    "#buyingPriceValue>.priceLarge",
                    "#priceBlock .product .priceLarge",
                    "#olpDivId .price",
                    "#priceblock_ourprice",
                    "#priceblock_saleprice",
                    "#unqualifiedBuyBox .a-color-price",
                    "#soldByThirdParty .a-color-price",
                    "#ags_price_local"
                ],
                "name": [
                    ".parseasinTitle>#btAsinTitle>span",
                    ".parseasinTitle>span",
                    "#btAsinTitle",
                    "#productTitle"
                ],
                "url": [
                    "^http://www.amazon.cn/(.*/)?(gp/product/|dp/|mn/detailApp).*"
                ]
            },
            "apple.com": {
                "price": [
                    "[itemprop='price']",
                    "#purchase-info-primary .value:first"
                ],
                "name": [
                    "div#title>h1",
                    ".section-product-title h3:first",
                    "#primary-main-content .title"
                ],
                "url": [
                    "^http://store.apple.com/cn[-_a-zA-Z0-9]*/product/.*",
                    "^http://store.apple.com/cn[-_a-zA-Z0-9]*/buy-[a-z]+/.*product=[a-zA-Z0-9]+"
                ]
            },
            "benlai.com": {
                "price": [
                    ".newprice:last"
                ],
                "name": [
                    "#Product_ProductDetailsName"
                ],
                "url": [
                    "^http://www.benlai.com/item-\\d+.html"
                ]
            },
            "china-pub.com": {
                "price": [
                    ".pro_buy_sen"
                ],
                "name": [
                    ".pro_book>h1"
                ],
                "url": [
                    "^http://product.china-pub.com/[0-9]+.*"
                ]
            },
            "coo8.com": {
                "price": [
                    ".c8-cxprice>em:not([class])",
                    ".c8-utxt>.c8-money"
                ],
                "name": [
                    "#prdtitle>h1"
                ],
                "url": [
                    "^http://www\\.coo8\\.com/product/[A-Za-z0-9]+\\.html.*"
                ]
            },
            "coolpad.com": {
                "price": [
                    ".produce_scall_right_textx:first"
                ],
                "name": [
                    ".good_name h1"
                ],
                "url": [
                    "^http://www\\.coolpad\\.com/goods/[0-9]+\\.html"
                ]
            },
            "dangdang.com": {
                "price": [
                    "#promo_price",
                    "#d_price",
                    "#salePriceTag"
                ],
                "name": [
                    ".head>h1"
                ],
                "url": [
                    "^http://product\\.dangdang\\.com/(main/)?[Pp]roduct\\.aspx.*",
                    "^http://product.dangdang.com/[0-9]+.html"
                ]
            },
            "dianping.com": {
                "price": [
                    ".buy-bottom-price:first"
                ],
                "name": [
                    ".deal-title h1:first"
                ],
                "url": [
                    "^http://t.dianping.com/deal/\\d+"
                ]
            },
            "book.douban.com": {
                "price": [],
                "name": [
                    "#wrapper>h1"
                ],
                "url": [
                    "http://book.douban.com/subject/[0-9]+/$"
                ]
            },
            "ehaier.com": {
                "price": [
                    ".cur-price"
                ],
                "name": [
                    ".product-title"
                ],
                "url": [
                    "^http://www.ehaier.com/product/\\d+.html"
                ]
            },
            "etao.com": {
                "price": [
                    ".original-price",
                    ".J_price",
                    ".real-price-num"
                ],
                "name": [
                    "strong.product-name",
                    "h1.top-title",
                    "title"
                ],
                "url": [
                    "^http://s.etao.com/detail/[0-9]+.html",
                    "^http://detail.etao.com/[0-9]+.htm",
                    "^http://detail.etao.com/item.htm"
                ]
            },
            "fclub.cn": {
                "price": [
                    ".goods_price strong:first"
                ],
                "name": [
                    ".goods_introduce h3:first"
                ],
                "url": [
                    "^http://www.fclub.cn/goods-\\d+"
                ]
            },
            "feiniu.com": {
                "price": [
                    ".ssm_price:first"
                ],
                "name": [
                    "#pro_title"
                ],
                "url": [
                    "^http://www.feiniu.com/item/[0-9a-zA-Z]+"
                ]
            },
            "fruitday.com": {
                "price": [
                    ".prod_price:first"
                ],
                "name": [
                    ".cp-ming01:first"
                ],
                "url": [
                    "^http://www.fruitday.com/web/pro/\\d+"
                ]
            },
            "gome.com.cn": {
                "price": [
                    ".detail .price",
                    ".actions .price",
                    ".tuan-info .item-buy",
                    "#salePrice",
                    "#prdPrice"
                ],
                "name": [
                    "#prdtitle>h1",
                    ".prdtit",
                    ".product-info .name",
                    ".tuan-item .name",
                    ".grdsd-tit"
                ],
                "url": [
                    "^http://www.gome.com.cn/ec/homeus/jump/product/\\d+\\.html.*",
                    "^http://www.gome.com.cn/product/([0-9]+)-([0-9]+)\\.html.*",
                    "^http://www.gome.com.cn/product/([0-9]+)\\.html.*",
                    "^http://www\\.gome\\.com.cn/product/[-A-Za-z0-9]+\\.html.*",
                    "^http://item.gome.com.cn/[-A-Za-z0-9]+.html",
                    "^http://www.gome.com.cn/product/([0-9]+)-([0-9]+)\\.html.*",
                    "^http://www.gome.com.cn/ec/homeus/jump/product/\\d+\\.html.*",
                    "^http://www.gome.com.cn/ec/homeus/browse/productDetailSingleSku.jsp?.*?productId=\\d+.*",
                    "^http://www.gome.com.cn/ec/rushbuy/limitbuy/itemdetail/includeDetail.jsp\\?limitBuyItemId=[0-9]+",
                    "^http://tuan.gome.com.cn/deal/\\w+.html"
                ]
            },
            "handu.com": {
                "price": [
                    ".promote_price:first",
                    ".market_price:first"
                ],
                "name": [
                    "title",
                    ".product_name:first"
                ],
                "url": [
                    "^http://www.handu.com/goods-\\d+.html"
                ]
            },
            "hitao.com": {
                "price": [
                    ".newprc:first",
                    ".price em"
                ],
                "name": [
                    ".product-titles h2:first",
                    ".tuan_name"
                ],
                "url": [
                    "^http://new.hitao.com/product-\\d+.html",
                    "^http://www.hitao.com/product-\\d+.html"
                ]
            },
            "homevv.com": {
                "price": [
                    "th_price_t",
                    "#rushLable_price",
                    "#price_cankao"
                ],
                "name": [
                    ".Pro_pageTitle"
                ],
                "url": [
                    "^http://www.homevv.com/vvshopProductView/pid-[0-9]+.*"
                ]
            },
            "j1.com": {
                "price": [
                    "#jianyiPrice"
                ],
                "name": [
                    ".productarea-right-1 h1",
                    ".detailnav span strong"
                ],
                "url": [
                    "^http://www.j1.com/product/\\d+-\\d+.html"
                ]
            },
            "jd.com": {
                "price": [
                    "#jd-price",
                    "#summary-price>.dd>strong",
                    "#priceinfo",
                    ".p-name .p-price:first",
                    ".l_info_a b:first"
                ],
                "name": [
                    "#name>h1",
                    "#name>h2",
                    ".mc h2:first",
                    ".l_info_name h5:first"
                ],
                "url": [
                    "^http://item\\.jd\\.com/(product/)?[0-9]+\\.html.*",
                    "^http://www\\.jd\\.com/product/[0-9]+\\.html.*",
                    "^http://(book|mvd|e|music)\\.jd\\.com/[0-9]+\\.html.*",
                    "^http://tuan.jd.com/team-\\d+.html",
                    "^http://re.jd.com/cps/item/[0-9]+.html"
                ]
            },
            "jiuxian.com": {
                "price": [
                    "#_nowPriceStr",
                    "#actPricePrice",
                    ".jx_price",
                    "#shopPricePrice"
                ],
                "name": [
                    ".det-cur",
                    ".detail-depict > .depict-name > h3"
                ],
                "url": [
                    "^http://www.jiuxian.com/goods-[0-9]+.*"
                ]
            },
            "jumei.com": {
                "price": [
                    ".newdeal_deal_price",
                    "#deal_info .buyit",
                    "#mall_price",
                    ".price_now"
                ],
                "name": [
                    ".newdeal_breadcrumbs_wrap_b",
                    ".share_title",
                    "#detail_top > .title > span",
                    ".breadcrumbs a:last",
                    ".pop_detail_tit"
                ],
                "url": [
                    "^http://\\w+.jumei.com/i/deal/\\w+.html",
                    "^http://mall.jumei.com/(.*/)*product_\\d+.html"
                ]
            },
            "lefeng.com": {
                "price": [
                    ".song>b:first-child"
                ],
                "name": [
                    ".pname"
                ],
                "url": [
                    "^http://product.lefeng.com/product/[0-9].*",
                    "^http://tuan.lefeng.com/[a-zA-Z]+/\\d+/[_0-9]+.html"
                ]
            },
            "m18.com": {
                "price": [
                    ".q_dcprice>dd>strong",
                    "#dl_sell_price>dd>strong",
                    ".groupbuy>.detailsArea>dd>p>strong"
                ],
                "name": [
                    ".goods_detail>.name"
                ],
                "url": [
                    "^http://list.m18.com/item/.*/[0-9]+.*",
                    "^http://list.m18.com/gmkt.inc/Goods/Goods.aspx\\?goodscode=[0-9]+.*"
                ]
            },
            "mbaobao.com": {
                "price": [
                    ".goods-price>.price-num"
                ],
                "name": [
                    ".goods-name"
                ],
                "url": [
                    "^http://www.mbaobao.com/item/[0-9].*"
                ]
            },
            "meilishuo.com": {
                "price": [
                    ".buy_info .price dt",
                    ".sku_meta .price"
                ],
                "name": [
                    ".s_tle"
                ],
                "url": [
                    "^http://www.meilishuo.com/share/item/\\d+",
                    "^http://www.meilishuo.com/prom/item/\\d+"
                ]
            },
            "mi.com": {
                "price": [
                    "#J_mi_goodsPrice",
                    ".J_mi_goodsPrice:first"
                ],
                "name": [
                    "#goodsName"
                ],
                "url": [
                    "^http://www.mi.com/goods/[0-9]+",
                    "^http://www.mi.com/item/[0-9]+",
                    "^http://item.mi.com/[0-9]+.html",
                    "^http://www.mi.com/[a-zA-Z0-9]+(/)?$",
					"^http://item.mi.com/buyphone/[a-zA-Z0-9]+(/)?$"
                ]
            },
            "mogujie.com": {
                "price": [
                    ".good_prs:first .red",
                    "#nowprice"
                ],
                "name": [
                    ".spus_title .txt.fl",
                    ".shoptitle"
                ],
                "url": [
                    "^http://www.mogujie.com/magic/spu/list/[a-z0-9]+",
                    "^http://www.mogujie.com/trade/goods/detail/[a-z0-9]+",
                    "^http://shop.mogujie.com/detail/[a-z0-9]+"
                ]
            },
            "moonbasa.com": {
                "price": [
                    "#p_saleprice"
                ],
                "name": [
                    ".p_info>h2:first-child"
                ],
                "url": [
                    "^http://[a-z]+.moonbasa.com/p-[0-9]+.*"
                ]
            },
            "muyingzhijia.com": {
                "price": [
                    "#iteminfo .f_price strong"
                ],
                "name": [
                    ".productDe001s"
                ],
                "url": [
                    "^http://www.muyingzhijia.com/product/[0-9]+"
                ]
            },
            "newegg.cn": {
                "price": [
                    "#hiddenProductPrice"
                ],
                "name": [
                    "#productTitle h1"
                ],
                "url": [
                    "^http://www.newegg.cn/[Pp]roduct/[-_0-9A-Za-z]+.htm.*"
                ]
            },
            "no5.com.cn": {
                "price": [
                    "#sPriVL",
                    ".n_neir span:first"
                ],
                "name": [
                    ".p01_r h2:first"
                ],
                "url": [
                    "^http://www.no5.com.cn/product/\\d+.html"
                ]
            },
            "ocj.com.cn": {
                "price": [
                    ".info_box .price:first",
                    ".product_detail .price:first"
                ],
                "name": [
                    ".pv_shop_detail_title h1:first",
                    ".product-info .title:first"
                ],
                "url": [
                    "^http://www.ocj.com.cn/detail/\\d+",
                    "^http://www.ocj.com.cn/otuans/detail/\\d+"
                ]
            },
            "okbuy.com": {
                "price": [
                    "#prodPriceAj"
                ],
                "name": [
                    ".prodAllName:first"
                ],
                "url": [
                    "^http://www.okbuy.com/.*/detail(/)?[_-a-zA-Z0-9]+\.html"
                ]
            },
            "paixie.net": {
                "price": [
                    "#js_current_price"
                ],
                "name": [
                    "#proinfo>h1:first-child"
                ],
                "url": [
                    "^http://www.paixie.net/shoe-.*"
                ]
            },
            "pchome.net": {
                "price": [
                    ".shops-price a:first",
                    ".parameter .price:first"
                ],
                "name": [
                    ".top_big_title h1:first"
                ],
                "url": [
                    "^http://product.pchome.net/(.*/)*[0-9]+.html"
                ]
            },
            "pconline.com.cn": {
                "price": [
                    "#price_current:first",
                    ".paramWrap .price:first"
                ],
                "name": [
                    ".sTit h1:first",
                    ".pro-param .hd h1:first"
                ],
                "url": [
                    "^http://product.pconline.com.cn/(.*/)*[0-9]+.html"
                ]
            },
            "sfbest.com": {
                "price": [
                    "#price-sf .price"
                ],
                "name": [
                    ".pItemsName h1"
                ],
                "url": [
                    "^http://www.sfbest.com/html/products/[0-9]+/[0-9]+\\.html"
                ]
            },
            "shangpin.com": {
                "price": [
                    ".spDetail_price_mark:first"
                ],
                "name": [
                    "#spDetail_proInfo h1:first"
                ],
                "url": [
                    "^http://www.shangpin.com(/.*)?/product(/.*)?/\\d+"
                ]
            },
            "suning.com": {
                "price": [
                    "#mainPrice>em",
                    "#netPrice>em",
                    ".main-price>em",
                    ".group-price",
                    "#rpPrice",
                    "#promotionPrice",
                    "#promoPrice",
                    ".detail-info .price strong:first"
                ],
                "name": [
                    ".pro_title span",
                    ".product-main-title > h1.wb",
                    "#itemDisplayName",
                    "#productDisplayName",
                    ".detail-info h2:first"
                ],
                "url": [
                    "^http://www\\.suning\\.com/emall/\\w+.html",
                    "^http://product.suning.com/([0-9]+/)*(detail)?[-_0-9]+.html",
                    "^http://qiang.suning.com/rps-web/rp/showActivity_[0-9]+.*",
                    "^http://product.suning.com/snupgbpv_.*.html",
                    "^http://ju.suning.com/product-[0-9]+.htm"
                ]
            },
            "taobao.com": {
                "price": [
                    "#J_PromoPrice .tb-rmb-num",
                    ".tb-rmb-num:first",
                    "#J_StrPrice",
                    ".currentPrice.floatleft",
                    ".price-block span",
                    ".price-block .price.big",
                    ".detail-info .title .price:first",
                    "#J_Property .price",
                    ".currentPrice:first"   // http://detail.ju.taobao.com/home.htm?item_id=40505026756
                ],
                "name": [
                    "#J_Title h3",
                    ".tb-detail-hd h3",
                    ".tb-item-title h3",
                    ".top_info .hd h2",
                    ".name-box .name",
                    "#J_Property .title",
                    ".detail-info .hd h1",
                    ".J_mainBox .title:first"   // http://detail.ju.taobao.com/home.htm?item_id=40505026756
                ],
                "url": [
                    "^http://item\\.taobao\\.com/item\\.htm.*",
                    "^http://wt\\.taobao\\.com/detail\\.htm?.*",
                    "^http://detail\\.ju\\.taobao\\.com/home\\.htm.+id=",
                    "^http://shuziitem\\.taobao\\.com/item\\.htm",
                    "^http://2\\.taobao\\.com/item\\.htm",
                    "^http://spu.taobao.com/.*spuid=[0-9]+.*"
                ]
            },
            "taoxie.com": {
                "price": [
                    ".d-real-price:first"
                ],
                "name": [
                    ".d-name h1:first"
                ],
                "url": [
                    "^http://www.taoxie.com/commodity-\\d+"
                ]
            },
            "tiantian.com": {
                "price": [
                    "#seckillprice:first",
                    ".xx_price:first"
                ],
                "name": [
                    ".detail_mbx a:last"
                ],
                "url": [
                    "^http://www.tiantian.com/cosmetic/A?[0-9]+\\.html"
                ]
            },
            "tmall.com": {
                "price": [
                    "#J_PromoBox>.J_CurPrice",
                    "#J_StrPrice",
                    "#J_PromoBox .tb-wrTuan-fullPaymen",
                    "#J_PromoBox .tb-wrTuan-num",
                    ".tm-price:first"
                ],
                "name": [
                    ".tb-detail-hd h3 a",
                    ".tb-detail-hd>h3",
                    ".tb-detail-hd h1"
                ],
                "url": [
                    "^http://(m)?detail\\.tmall\\.com/item\\.htm.*",
                    "^http://chaoshi.detail\\.tmall\\.com/item\\.htm.*"
                ]
            },
            "vancl.com": {
                "price": [
                    ".cuxiaoPrice>.tehuiMoney strong"
                ],
                "name": [
                    "#productTitle>h2"
                ],
                "url": [
                    "^http://item\\.vancl\\.com/[0-9]+\\.html.*"
                ]
            },
            "vip.com": {
                "price": [
                    ".goods_price_sale",
                    ".pbox_price > em",
                    ".rci_head",
                    ".bt_infos_price",
                    ".shan_price strong:first",
                    ".pbox-price:first"
                ],
                "name": [
                    ".goods_protit",
                    ".pib_title",
                    ".bt_top_title",
                    ".bt_crumbs span",
                    ".shan_description p strong:first",
                    ".pib-title-detail:first"
                ],
                "url": [
                    "^http://\\w+.vip.com/detail[-0-9]+"
                ]
            },
            "vjia.com": {
                "price": [
                    "#SpecialPrice"
                ],
                "name": [
                    ".title"
                ],
                "url": [
                    "^http://item.vjia.com/[0-9]+.html.*"
                ]
            },
            "vmall.com": {
                "price": [
                    "#pro-price b"
                ],
                "name": [
                    "#pro-name"
                ],
                "url": [
                    "^http://www.vmall.com/product/[0-9]+.*"
                ]
            },
            "wanggou.com": {
                "price": [
                    "#commodityCurrentPrice"
                ],
                "name": [
                    ".pp_prop_tit>.pp_prop_fn"
                ],
                "url": [
                    "^http://item.wanggou.com/.*"
                ]
            },
            "wbiao.cn": {
                "price": [
                    "b#price:first"
                ],
                "name": [
                    ".cpname h1:first"
                ],
                "url": [
                    "^http://www.wbiao.cn/.+-g\\d+.html"
                ]
            },
            "winxuan.com": {
                "price": [
                    ".price_info>li:first-child>.fb"
                ],
                "name": [
                    ".goods_title"
                ],
                "url": [
                    "^http://www.winxuan.com/product/[0-9]+.*"
                ]
            },
            "wl.cn": {
                "price": [
                    ".lh.wl"
                ],
                "name": [
                    ".pro.blankbtm h1"
                ],
                "url": [
                    "^http://www.wl.cn/\\d+"
                ]
            },
            "womai.com": {
                "price": [
                    "#combiProductBuyPrice",
                    "#buyPrice",
                    ".buyprice:first"
                ],
                "name": [
                    ".pro_tit_top_forcombi",
                    ".pro_tit_top",
                    ".detail_goods_cont h1",
                    ".WrapTit:first"
                ],
                "url": [
                    "^http://.*.womai.com/related-[0-9]+-[0-9]+.*",
                    "^http://.*.womai.com/Product-[0-9]+-[0-9]+.*",
                    "^http://.*.womai.com/seller/product-[0-9]+-[0-9]+.*",
                    "^http://.*.womai.com/PackBuyProduct-[0-9]+-[0-9]+.htm",
                    "^http://jiu.womai.com/Wine/Product/Product-\\d+-\\d+.htm"
                ]
            },
            "xiu.com": {
                "price": [
                    "#prd_price_div .style1",
                    "#prd_price_div .style2",
                    "#prd_price_div .style3",
                    "#prd_price_div .style4",
                    "#prd_price_div .style5",
                    "#prd_price_div .style6",
                    ".xit_fudong span"
                ],
                "name": [
                    ".p_title span:first",
                    ".xit_xqzgong h2"
                ],
                "url": [
                    "^http://item.xiu.com/product/[0-9]+.shtml",
                    "^http://tuan.xiu.com/team_[0-9]+.html",
                    "^http://ebay.xiu.com/product/[0-9]+.shtml",
                    "^http://outlets.xiu.com/[0-9]+.shtml"
                ]
            },
            "yesky.com": {
                "price": [
                    ".gbckjg dd strong:first",
                    ".paramWrap .price:first",
                    ".pricename_bj ul li span strong:first",
                    ".buyshop .bj span:first"
                ],
                "name": [
                    ".gbright h2:first",
                    ".pro_name h1:first"
                ],
                "url": [
                    "^http://product.yesky.com/product/([0-9]*/)+((index|price|buy)(_[0-9]+)?.shtml)?"
                ]
            },
            "yesmywine.com": {
                "price": [
                    ".myPrice em:first",
                    ".ymPrice em:first"
                ],
                "name": [
                    ".pro-name h1:first"
                ],
                "url": [
                    "^http://www.yesmywine.com/goods/\\d+.html"
                ]
            },
            "yhd.com": {
                "price": [
                    "#current_price",
                    "#pricenow:first"
                ],
                "name": [
                    "#productMainName",
                    ".unit_tit h1:first"
                ],
                "url": [
                    "^http://item\\.yhd\\.com/item/.*",
                    "^http://t.yhd.com/detail/\\d+"
                ]
            },
            "yiguo.com": {
                "price": [
                    ".tabs_info .cxj:first"
                ],
                "name": [
                    ".cpname h1:first"
                ],
                "url": [
                    "^http://www.yiguo.com/product/\\d+.html"
                ]
            },
            "yintai.com": {
                "price": [
                    ".yt-num"
                ],
                "name": [
                    ".p-tit"
                ],
                "url": [
                    "^http://item.yintai.com/[0-9A-Z]+-[0-9A-Z]+-[0-9A-Z].*"
                ]
            },
            "yixun.com": {
                "price": [
                    ".xbase_col2>.mod_price[itemprop='lowPrice']",
                    ".xbase_col2>.mod_price"
                ],
                "name": [
                    ".xbase_row1>.xname"
                ],
                "url": [
                    "^http://item.yixun.com/item-[0-9]+.html.*"
                ]
            },
            "yougou.com": {
                "price": [
                    ".itm_bd>.price",
                    "#yitianPrice"
                ],
                "name": [
                    ".goodsCon>h1:first-child"
                ],
                "url": [
                    "^http://www.yougou.com/.*/sku-[a-z0-9]+-[0-9]+.*"
                ]
            },
            "yummy77.com": {
                "price": [
                    ".cprice .price:first",
                    ".pprice .price:first"
                ],
                "name": [
                    ".divpname .pdesc:first"
                ],
                "url": [
                    "^http://www.yummy77.com/product/\\d+.html"
                ]
            },
            "zhiwo.com": {
                "price": [
                    ".mumer"
                ],
                "name": [
                    "h1.title"
                ],
                "url": [
                    "^http://www.zhiwo.com/product/\\d+"
                ]
            },
            "zol.com.cn": {
                "price": [
                    "#b2cPriceUl .onlyone em:last",
                    ".product-b2c-price>li>span:first",
                    ".price-type:first",
                    ".price-num:first"
                ],
                "name": [
                    ".product-name h3:first",
                    ".ptitle h1:first"
                ],
                "url": [
                    "^http://detail.zol.com.cn/(.*/)*index[0-9]+.shtml",
                    "^http://detail.zol.com.cn/series/[0-9]+/[_0-9]+.html"
                ]
            }
        };

        function isTargetPage(url) {
            var hostname = parseUrl(url).hostname;
            var matchedHostname = undefined;
            for (var host in S.pattern) {
                if (('.' + hostname).indexOf('.' + host) !== -1) {
                    matchedHostname = host;
                    break;
                }
            }
            if (matchedHostname) {
                for (var i = 0; i < S.pattern[matchedHostname].url.length; i++) {
                    var urlRegex = S.pattern[matchedHostname].url[i];
                    if (new RegExp(urlRegex, 'gi').test(url))
                        return true;
                }
            }
            return false;
        }

        var mergedHosts = hosts.concat(Object.keys(S.pattern));

        var matchedHostname = undefined;
        for (var i = 0; i < mergedHosts.length; i++) {
            if (('.' + hostname).indexOf('.' + mergedHosts[i]) !== -1) {
                matchedHostname = mergedHosts[i];
                break;
            }
        }

        function loadJSForMatchedURL() {
            _gaq.push(['favormy._trackEvent', 'MatchedURL', window.location.host, url]);
            S.loadJS(S.Constants.S_SERVER + "scripts/jquery.fm.min.js", function() {
                S.loadJS(S.Constants.S_SERVER + "scripts/enhancement.js", function() {
                    S.loadJS(S.Constants.S_SERVER + "scripts/favormy.js", function() {

                    });
                });
            });
        }

        if (matchedHostname) {
            if (isTargetPage(url)) {
                loadJSForMatchedURL();
            } else if (Math.random() > 0.99) {
                S.fallbackMatchedURL = true;
                loadJSForMatchedURL();
            }
        } else if (Math.random() > 0.999) {
            S.fallbackMatchedURL = true;
            loadJSForMatchedURL();
        }
    }
})(_com_favormy_plugin, window);