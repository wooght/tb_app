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
                // console.log(`custom run ryw.a: hashMap=${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
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
    }else{
        console.log('hook 失败')
    }
    // var ClassName=Java.use("com.luoye.test.ClassName");
    // var instance = ClassName.$new();

    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
        // var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        // console.log('start:' + ret)
        return false;
    };

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
    var is_set_hm = false       // 是否已经设置hasmMap
    var hhmm = MapH.$new()      // 构造一个map对象
    var hhmm2 = MapH.$new()
    var request_form
    // Object.keys(hm).forEach(function(k){
    //     hhmm.put(k, hm[k])
    // })
    // // hhmm.remove('extdata')
    // // hhmm.put('extdata', hhmm.get('openappkey'))

    // Object.keys(hm2).forEach(function(k){
    //     hhmm2.put(k, hm2[k])
    // })
    // console.log(`${hhmm}`)

    // recv POST传递访问函数
    recv('poke', function onMessage(pokeMessage) {
        console.log('poke called...')
        console.log('recv(pokie) run:', pokeMessage.data)
        sign_params = pokeMessage.data
        now_time = pokeMessage.now_time
    });
    recv('sign',function onMessage(pokeMessage) {
        console.log('call start ')
        console.log(`native data: ${hhmm.get('data')}`)
        console.log(`send data:${pokeMessage.data}`)
        if(is_set_hm){
            console.log('call here')
            hhmm.remove('data')
            hhmm.put('data', pokeMessage.data)
            hhmm.remove('t')
            hhmm.put('t', pokeMessage.now_time)
            st3 = pokeMessage.st3
            var sign_result = call_new_sign(hhmm, hhmm2, st, st2 ,zz, pokeMessage.st3)
            var falcoid = get_falcoId()
            send({'type':'sign','data':`${sign_result}`, 'falcoid':falcoid, 'form_data':hhmm.get('data').toString(), 't':t})
        }else{
            send({'type':'error', 'data':'is_set_hm false'})
        }
    });

    /**
     * 设置详情页请求数据格式
     */
    var set_detail_hm = function(){
        // hm['api'] = 'mtop.taobao.detail.data.get'
        // hm['']
        // 详情页 修改api及其他参数
        is_set_hm = true
        hhmm.remove('api')
        hhmm.put('api', 'mtop.taobao.detail.data.get')
        hhmm.put('x-accept-stream', 'true')
        console.log(hhmm.get('api'))
    }

    /**
     * 调用app 函数,获取sign等签名数据
     * @param {*} txt 
     * @param {*} now_time 
     * @param {*} s 
     * @returns 
     */
    var extract_sign = function(hm_structure, hashMap_data, now_time, s){
        if(is_set_hm){
            console.log('CALL EXTRACT_SIGN......')
            var hm = MapH.$new()                    // hashMap native
            var hm_json = JSON.parse(hm_structure)  // hashMap json
            Object.entries(hm_structure).forEach(function([key, val]){
                hm.put(key, val)
            })
            hm.remove('data')
            hm.put('data', hashMap_data)       // 设置当前请求内容
            hm.remove('t')            
            hm.put('t', now_time)     // 设置当前请求时间
            st3 = s
            var sign_result = call_new_sign(hm, hhmm2, st, st2 ,zz, st3)
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
        setDetailHm:set_detail_hm,
        getAppSign:extract_sign
    }

    // function get_new_map(){
    //     Java.cast({'data':123},MapH)
    // }

    /**
     * 获取正常访问的hashMap
     * 设置新的hashMap
     */
    function set_hhmm(hashMap){
        hhmm.remove('sid')
        hhmm.put('sid', hashMap.get('sid'))         
        hhmm.remove('deviceId')
        hhmm.put('deviceId', hashMap.get('deviceId'))
        hhmm.remove('utdid')
        hhmm.put('utdid', hashMap.get('utdid'))
        hhmm.remove('lat')
        hhmm.put('lat', hashMap.get('lat'))
        hhmm.remove('lng')
        hhmm.put('lng', hashMap.get('lng'))
    }

    /**
     * hook ryw 调用sign生成函数
     */
    let ryw = Java.use("tb.ryw")
    ryw["a"].overload('java.util.HashMap', 'java.util.HashMap', 'java.lang.String', 'java.lang.String', 'boolean', 'java.lang.String').implementation = function (hashMap, hashMap2, str, str2, z, str3) {
        if(hashMap.get('api') == 'mtop.taobao.wireless.home.category' || hashMap.get('api') == 'mtop.taobao.detail.data.get'){
            // console.log(`run hashMap:${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`)
            if(!is_set_hm){
                // 复制 appKey
                // st = str.toString()
                var hashMap_keys = mapKey(hashMap)
                console.log(`hashMap_keys${hashMap_keys}`)

                var hm_structure = {}
                // 复制hashMap  遍历数组
                hashMap_keys.forEach(function(key){
                    // hhmm.put(key, hashMap.get(key))
                    hm_structure[key] = hashMap.get(key).toString()
                })
                hm_structure['data'] = {}
                console.log(`hhmm:${hm_structure}`)

                var hm2_structure = {}
                // 复制hashMap2  遍历 字典
                Object.keys(hm2).forEach(function(key){
                    // hhmm2.put(key, hashMap2.get(key))
                    hm2[key] = hashMap2.get(key).toString()
                })
                // st3 = str3.toString()
                is_set_hm = true
                console.log(`is_set_hm set True:hashMap=${JSON.stringify(hm_structure)}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
                send({'type':'hashMap_data', 'hm_structure':`${JSON.stringify(hm_structure)}`, 'hm2_structure':`${JSON.stringify(hm2_structure)}`, 'hashMap_data':`${hashMap.get('data')}`})
            }
        }
        // native 运行
        let result = this["a"](hashMap, hashMap2, str, str2, z, str3);
        return result;
    };

    // 是否已经发送cookie,headers
    var send_cookie = false
    var send_headers = false

    let CookieManager = Java.use("anetwork.channel.cookie.CookieManager");
    // result Request 请求带的cookies
    CookieManager["getCookie"].implementation = function (str) {
        // console.log(`CookieManager.getCookie is called: str=${str}`);
        let result = this["getCookie"](str);
        if(allow_request(str)){
            if (!send_cookie){
                send({'type':'cookies', 'cookies':`${result}`});
                send_cookie = false;
        }}
        return result;
    };
    // c24666a 为Request,response 的综合内容
    let rye = Java.use("tb.rye");
    rye["a"].overload('mtopsdk.framework.domain.a').implementation = function (c24666a) {
        // c24666a.k 为 Request = Java.use("mtopsdk.network.domain.Request");
        if(allow_api.indexOf(c24666a.k.value.r.value) != -1){
            if (!send_headers){
                console.log(c24666a.k.value.c.value)
                send({'type':'headers', 'headers':mapString(c24666a.k.value.c.value), 'api':c24666a.k.value.r.value})
                send_headers = false;
        }}
        let result = this["a"](c24666a);
        return result;
    };
});