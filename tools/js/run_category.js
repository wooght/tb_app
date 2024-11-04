/**
 * 触发函数 获取sign 等签名
 * @param {*} hashMap 
 * @param {*} hashMap2 
 * @param {*} str 
 * @param {*} str2 
 * @param {*} z 
 * @param {*} str3 
 * @returns String
 */
function call_new_sign(hashMap, hashMap2, str, str2, z, str3){
    /**
     * 触发函数 获取sign 等签名
     */
    var ryw = Java.use("tb.ryw")
    var result_sign
    Java.perform(function(){
        Java.choose('tb.ryw', {
            onMatch: function(instance){
                console.log(`custom run ryw.a: hashMap=${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
                result_sign = instance['a'](hashMap, hashMap2, str, str2, z, str3)
            },
            onComplete:function(){
                var a = 1
            }
        })
    })
    return result_sign
}

/**
 * 触发函数 获取falcoId
 * @returns falcoId
 */
function get_falcoId(){
    var result = ''
    var FullTraceAnalysis = Java.use("com.taobao.analysis.fulltrace.FullTraceAnalysis");
    Java.perform(function(){
        Java.choose('com.taobao.analysis.fulltrace.FullTraceAnalysis', {
            onMatch: function(instance){
                result = instance['createRequest']('mtop')
                // console.log('new falcoId:', result)
            },
            onComplete: function(){
                // console.log('get falcoId end')
            }
        });
    });
    return result
}
/**
 * map 转String
 * @param {*} map 
 * @returns String
 */
function mapString(map){
    /**
     * map 转String
     */
    var entrySet = map.entrySet();
    var iterator = entrySet.iterator();
    var map_arr = []
    while (iterator.hasNext()){
        map_arr.push(iterator.next())
    }
    return map_arr.join('|||')
}

/**
 * 返回Map的keys
 * @param {*} map 
 * @returns 
 */
function mapKey(map){
    var entrySet = map.entrySet();
    var iterator = entrySet.iterator();
    var map_arr = []
    while (iterator.hasNext()){
        map_arr.push(iterator.next().toString().split('=')[0])
    }
    console.log(`mapKey:${map_arr}`)
    return map_arr
}
// 要进行判断的Request api
var allow_api = ['mtop.taobao.wireless.home.newface.awesome.get',
                'mtop.taobao.wireless.home.category',
                'mtop.taobao.detail.data.get']

/**
 * 进行cookies,Request判断的Request
 * @param {*} url 
 * @returns 
 */
function allow_request(url){
    var is_allow = false
    allow_api.forEach(function(api){
        if(url.indexOf(api) != -1 ){
            is_allow = true
        }
    })
    return is_allow
}
Java.perform(function () {
    if(Java.available){
        console.log("Android Version:",Java.androidVersion);
    }
    // var ClassName=Java.use("com.luoye.test.ClassName");
    // var instance = ClassName.$new();

    // var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    // SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
    //     // var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
    //     // console.log('start:' + ret)
    //     return false;
    // };

    /**
     * hashMap 初始化
     */
    var MapH = Java.use('java.util.HashMap')
    // var hm1 = {
    //     "deviceId":"AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF",
    //     "sid"="25601ccd9fad1321ce4f2a5cebbd86dd",
    //     "uid"="4060247732", "x-features"="27", "appKey"="21646297", "api"="mtop.taobao.wireless.home.category", "lat"="39.633542", "lng"="115.109334", "mtopBusiness"=true, "utdid"="Zs7Pnkn0r40DAKSy/CBlF7cX", "extdata"=openappkey=DEFAULT_AUTH, ttid=703304@taobao_android_10.39.10, t=1726655388, v=1.0
    // }
    var sign_params = ''
    var now_time = ''
    // 详情页hm 有 x-accept-stream=true 在ttid后面,详情页 api:mtop.taobao.detail.data.get
    var hm = {'data':'', 'deviceId': 'AoTOR-m0gtRFpKfeFl72Zhs1sBg2ah8yk1e4IJZM34K7', 'sid': '259eb332af61da7d471e84729aa845d4', 'uid': '4060247732', 'x-features': '27', 'appKey': '21646297', 'api': 'mtop.taobao.wireless.home.category', 'lat': '23.178220039218854', 'lng': '113.41819508536969', 'mtopBusiness': 'true', 'utdid': 'ZwEjaAswd6ADALux5YmWEFpd', "extdata":"openappkey=DEFAULT_AUTH", 'ttid': '703304@taobao_android_10.39.10', 't': '1726655388', 'v': '1.0'}
    var hm_d = {'data':'', 'deviceId': 'AoTOR-m0gtRFpKfeFl72Zhs1sBg2ah8yk1e4IJZM34K7', 'sid': '259eb332af61da7d471e84729aa845d4', 'uid': '4060247732', 'x-features': '27', 'appKey': '21646297', 'api': 'mtop.taobao.detail.data.get', 'lat': '23.178220039218854', 'lng': '113.41819508536969', 'mtopBusiness': 'true', 'utdid': 'ZwEjaAswd6ADALux5YmWEFpd', "extdata":"openappkey=DEFAULT_AUTH", 'ttid': '703304@taobao_android_10.39.10', 'x-accept-stream':'true', 't': '1726655388', 'v': '1.0'}

    var hm2 = {"pageId":"http://m.taobao.com/index.htm", "pageName":"com.taobao.tao.welcome.Welcome"}
    // 进行sign 计算需要的几个参数hashMap, hashMap2, st, st2, zz, st3
    var st = '21646297'     // appKey
    var st2 = null
    var zz = false          
    var st3                 // Request 次数

    var t
    var result_sign             // 需要返回的sign签名字符串
    var is_set_hm = true       // 是否已经设置hasmMap
    var hhmm = MapH.$new()      // 构造一个map对象
    var hhmm2 = MapH.$new()
    var request_form

    /**
     * 调用app 函数,获取sign等签名数据
     * @param {*} txt 
     * @param {*} now_time 
     * @param {*} s 
     * @returns 
     */
    var extract_sign = function(hm_structure, hm2_structure, hashMap_data, now_time, s){
        if(is_set_hm){
            console.log('CALL EXTRACT_SIGN......')
            var hm = MapH.$new()                    // hashMap native
            var hm2 = MapH.$new()
            var hm_json = JSON.parse(hm_structure)  // hashMap json
            var hm2_json = JSON.parse(hm2_structure)
            Object.entries(hm_json).forEach(function([key, val]){
                hm.put(key, val.toString())
            })
            Object.entries(hm2_json).forEach(([key, val]) =>{
                hm2.put(key, `${val}`)
            })
            hm.remove('data')
            hm.put('data', hashMap_data)       // 设置当前请求内容
            hm.remove('t')            
            hm.put('t', now_time)     // 设置当前请求时间
            st3 = s
            var sign_result = call_new_sign(hm, hm2, st, st2 ,zz, st3)
            var falcoid = get_falcoId()
            console.log(`${sign_result}`)
            return {'data':`${sign_result}`, 'falcoid':falcoid, 'form_data':hm.get('data').toString(), 't':t}
        }else{
            console.log('false is_set_hm')
            return {'type':'error', 'data':'is_set_hm false'}
        }
    }
    /**
     * rpc 接口 访问函数接口 
     * */ 
    rpc.exports = {
        getAppSign:extract_sign,
        // setDetailHm:set_detail_hm
    }
});

/**
 * {"nick":"锋鸿志远","tryRequest":"false","poiRefreshTime":"0","globalLbs":"{\"globalAreaCode\":\"510108\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.697662\",\"globalLng\":\"104.184410\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510108016\"}","countryCode":"CN","utdid":"ZwzvF2Swb/gDAK2RdMwOnx2v","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":1730726272501,\"bizParams\":{\"clickId\":\"\",\"currentExposureItemID\":\"\",\"currentRequestType\":\"scrollNextPage\",\"deviceLevel\":\"m\",\"firstPagePVID\":\"91a57abf-d811-451c-80be-f9085266c5ca\",\"guessChannelId\":\"pindao_baihuo\",\"hundredClickItemId\":\"798708328599\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"latestHundredItem\":\"827132933706,758060932383,653631925770,843027084904,770006118038,768720591599,781569727848,669195679146,742808742076,763437599060,741004225772,808632282188\",\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":0,\"clientReqTime\":1730726415548,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":1,\"isLastPage\":\"n\",\"itemLastCount\":\"12\",\"lastPage\":false,\"pageNum\":1,\"requestInAdvance\":2,\"virtualPageNum\":0},\"passParams\":{\"firstPagePVID\":\"91a57abf-d811-451c-80be-f9085266c5ca\",\"lastVersion\":\"v7\",\"nextPageBackupKeyPrefix\":\"prod_backup_88_2_5_smu:ul_3_android_10.39.10__pindao_baihuo\"},\"realBaseCacheTime\":0,\"requestType\":\"scrollNextPage\"}}","gatewayVersion":"2.0","userId":"574901677","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}
 * {"nick":"锋鸿志远","tryRequest":"false","poiRefreshTime":"0","globalLbs":"{\"globalAreaCode\":\"510108\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.697662\",\"globalLng\":\"104.184410\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510108016\"}","countryCode":"CN","utdid":"ZwzvF2Swb/gDAK2RdMwOnx2v","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":1730726139849,\"bizParams\":{\"clickId\":\"\",\"currentExposureItemID\":\"\",\"currentRequestType\":\"scrollNextPage\",\"deviceLevel\":\"m\",\"firstPagePVID\":\"c80117b5-1e02-4dc1-8e0d-d625ea166496\",\"guessChannelId\":\"pindao_baihuo\",\"hundredClickItemId\":\"731066063722\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"latestHundredItem\":\"626186177549,786570609680,739968527796,748619872765,602996536937,737507415717,740032734283,751897409525,541605605587,682542267940,811305261741,686719946181\",\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":0,\"clientReqTime\":1730726139998,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":1,\"isLastPage\":\"n\",\"itemLastCount\":\"38\",\"lastPage\":false,\"pageNum\":6,\"requestInAdvance\":6,\"virtualPageNum\":0},\"passParams\":{\"firstPagePVID\":\"c80117b5-1e02-4dc1-8e0d-d625ea166496\",\"lastVersion\":\"v7\",\"nextPageBackupKeyPrefix\":\"prod_backup_88_2_5_smu:ul_3_android_10.39.10__pindao_baihuo\"},\"realBaseCacheTime\":0,\"requestType\":\"scrollNextPage\"}}","gatewayVersion":"2.0","userId":"574901677","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}
 * {"nick":"锋鸿志远","tryRequest":"false","poiRefreshTime":"0","globalLbs":"{\"globalAreaCode\":\"510108\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.697662\",\"globalLng\":\"104.184410\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510108016\"}","countryCode":"CN","utdid":"ZwzvF2Swb/gDAK2RdMwOnx2v","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":1730726416393,\"bizParams\":{\"clickId\":\"\",\"currentExposureItemID\":\"\",\"currentRequestType\":\"scrollNextPage\",\"deviceLevel\":\"m\",\"firstPagePVID\":\"91a57abf-d811-451c-80be-f9085266c5ca\",\"guessChannelId\":\"pindao_baihuo\",\"hundredClickItemId\":\"798708328599\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"latestHundredItem\":\"802456975934,713461440145,624436047439,681372945394,627782817038,816747390135,659486479353,822447283052,592118098175,846473935231,811656856572,808632282188\",\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":0,\"clientReqTime\":1730726709663,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":-1,\"isLastPage\":\"n\",\"itemLastCount\":\"32\",\"lastPage\":false,\"pageNum\":2,\"requestInAdvance\":10,\"virtualPageNum\":0},\"passParams\":{\"firstPagePVID\":\"91a57abf-d811-451c-80be-f9085266c5ca\",\"lastVersion\":\"v7\",\"nextPageBackupKeyPrefix\":\"prod_backup_88_2_5_smu:ul_3_android_10.39.10__pindao_baihuo\"},\"realBaseCacheTime\":0,\"requestType\":\"scrollNextPage\"}}","gatewayVersion":"2.0","userId":"574901677","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}
 * {"nick":"锋鸿志远","tryRequest":"false","poiRefreshTime":"0","globalLbs":"{\"globalAreaCode\":\"510108\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.697662\",\"globalLng\":\"104.184410\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510108016\"}","countryCode":"CN","utdid":"ZwzvF2Swb/gDAK2RdMwOnx2v","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":1730726847991,\"bizParams\":{\"clickId\":\"\",\"currentExposureItemID\":\"\",\"currentRequestType\":\"scrollNextPage\",\"deviceLevel\":\"m\",\"firstPagePVID\":\"c80117b5-1e02-4dc1-8e0d-d625ea166496\",\"guessChannelId\":\"pindao_0001\",\"hundredClickItemId\":\"773813645222,579219777358,572383483184,704883655517,704883655517,542964321105,691156803586,558051894910,705514308152,676898311887,571828603878,731066063722\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"latestHundredItem\":\"700743775493,733858906056,647648746589,526433332392,684603481363,574715136171,711236192194,645830579588,724218876890,733032848575,821334353518,555961161012,662553379407,658303192024,745293068639,749025195124,27119772263,762656696596,608593528948,601632560678,714571869566,534099684321,688040862237,681710541183,754070282206,836015616640,825146890735,825211841614,613085512757,796734370755,739996511589,711963648773,714746585178,595100071061,654628633403,538302711411,8901383302,596241575309,680431576268,772478721643,662039478754,720719890622,798141213934,687859449459,41396529290,658467923152,761776474132,844384020131,679827890375,580302110183,732832621630,588044660080,662541274736,606566809612,734155741828,684545765867,598686091094,602289035942,551598108160,567738792991,794647745403,648893324567,692195608083,842026940814,626186177549,786570609680,739968527796,748619872765,602996536937,737507415717,740032734283,751897409525,541605605587,682542267940,811305261741,686719946181,804507583735,683989109317,613019593191,845055641142,619008745101,843880487788,662222107883,739143971732,653526948080,683459936235,679026792865,816416399682,797327500201,714293667695,726288800598,727451433060,615006227457,574903744894,739241407432,702949109963,688003915783,745228380138,840441189582,829790004854\",\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":0,\"clientReqTime\":1730726848032,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":-1,\"isLastPage\":\"n\",\"itemLastCount\":\"102\",\"lastPage\":false,\"pageNum\":17,\"requestInAdvance\":6,\"virtualPageNum\":0},\"passParams\":{\"firstPagePVID\":\"c80117b5-1e02-4dc1-8e0d-d625ea166496\",\"lastVersion\":\"v7\",\"nextPageBackupKeyPrefix\":\"prod_backup_88_2_5_smu:ul_3_android_10.39.10__pindao_0001\"},\"realBaseCacheTime\":0,\"requestType\":\"scrollNextPage\"}}","gatewayVersion":"2.0","userId":"574901677","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}
 */