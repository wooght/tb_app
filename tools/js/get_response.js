//import { get_caller_function } from './common_function.js';   // 报错:line 1: expecting '('
//const c = require('./common_function.js'); // 报错:ReferenceError: 'require' is not defined

function get_caller_function (obj){
    /**
     * 遍历运行栈队列/栈帖
     */
    var current_thread = Java.use('java.lang.Thread').currentThread();
    var stackTrace = current_thread.getStackTrace();
    console.log('\n==-==-stack trace start:')
    stackTrace.forEach(function(stackFrame){
        console.log(stackFrame.toString())
    })
    console.log('\n==-==-stack trace end')
}

function get_fields(c){
    /**
     * 遍历属性
     */
    // c.class.getFields().forEach(function(field){
    //     console.log('field${field}', c[field.name])
    // })
    // return c.class
    console.log('get_fields run:')
    Object.keys(c).forEach(function(key){
        console.log(`${key}:`, c[key].value)
    })
}

/**
 * 获取hashMap 的key值,返回array
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
    return map_arr
}
let hr = '==============================================';

Java.perform(function(){
    if(Java.available){
        console.log('Android version:', Java.androidVersion);
    }else{
        console.log('Hook faild')
    }

    // 关闭spdy 自定义协议
    let SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
        // var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        // console.log('start:' + ret)
        return false;
    };

    let hashMap = Java.use('java.util.HashMap')
    // 上一次数据
    var last_hashMap1 = hashMap.$new()
    var last_hashMap2 = hashMap.$new()
    var last_str = ''
    var last_str2 = null
    var last_z = false
    var last_str3 = ''
    var is_first = true

    /**
     * 获取hashMap 的key值,返回array
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
        return map_arr
    }

    /**
     * hashMap 对比
     * @param {*} last_hm 
     * @param {*} hm 
     */
    function hashMap_different(last_hm, hm){
        var hm_arr = mapKey(hm)
        hm_arr.forEach(function(key){
            if(last_hm.get(key).toString() != hm.get(key).toString()){
                console.log(`${key} is changed`)
                console.log(`last:${last_hm.get(key)}`)
                console.log(`new:${hm.get(key)}`)
            }
        })
    }
    /**
     * clone hashmap 避免hook变量不能持久化(app运行后内存清理)
     * @param {*} last_hm 
     * @param {*} hm 
     * @returns 
     */
    function clone_hashMap(last_hm, hm){
        var map_key = mapKey(hm)
        map_key.forEach(function(key){
            if(last_hm.containsKey(key)){
                last_hm.remove(key)
            }
            last_hm.put(key, hm.get(key))
        })
        return last_hm
    }
    /**
     * 获取参数变化
     * @param {} hashMap 
     * @param {*} hashMap2 
     * @param {*} str 
     * @param {*} str2 
     * @param {*} z 
     * @param {*} str3 
     */
    function is_change(hashMap, hashMap2, str, str2, z, str3){
        console.log('\n', hr)
        if(last_hashMap1 != hashMap){
            console.log('hashMap1 is change')
            hashMap_different(last_hashMap1, hashMap)
            last_hashMap1 = clone_hashMap(last_hashMap1, hashMap)
        }
        if(last_hashMap2 != hashMap2){
            console.log('hashMap2 is change')
            // last_hashMap2 = hashMap2
        }
        if(last_str != str){
            console.log(`str is change, last_str:${last_str}, new_str${str}`)
            last_str = str
        }
        if(last_str2 != str2){
            console.log(`str2 is change, last_str2:${last_str2}, new_str2${str2}`)
            last_str2 = str2
        }
        if(last_z != z){
            console.log(`z is change, last_z:${last_z}, new_z${z}`)
            last_z = z
        }
        if(last_str3 != str3){
            console.log(`str3 is change, last_str3:${last_str3}, new_str3${str3}`)
            last_str3 = str3
        }
        console.log(hr)
    }
    let rye = Java.use("tb.rye");
    rye["a"].overload('mtopsdk.framework.domain.a').implementation = function (c24666a) {
        console.log(c24666a.l.value)
        let result = this["a"](c24666a);
        // category api https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.category/1.0/
        // detail api
        if(c24666a.l.value == 'https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.category/1.0/'){

        //     console.log(`a:${c24666a.a.value}`)
        //     console.log(`b:${c24666a.b.value}`)
            console.log(`c:${c24666a.c.value}`)      // Response, detail 页面无内容, category页面有内容
        //     console.log(`d:${c24666a.d.value}`)
        //     console.log(`e:${c24666a.e.value}`)
        //     console.log(`g:${c24666a.f.value}`)
        //     console.log(`g:${c24666a.g.value}`)
        //     console.log(`h:${c24666a.h.value}`)
        //     console.log(`i:${c24666a.i.value.get('data')}`)      // POST 提交内容
        //     console.log(`j:${c24666a.j.value}`)
        //     console.log(`k:${c24666a.k.value}`)
            // console.log(`l:${c24666a.l.value}`)              // api 地址
        //     console.log(`m:${c24666a.m.value}`)
        //     var mapkey = mapKey(c24666a.m.value)
        //     mapkey.forEach(function(key){
        //         console.log(`${key}`, c24666a.m.value.get(key))
        //     })
        //     console.log(`n:${c24666a.n.value}`)
        //     console.log(`o:${c24666a.o.value}`)
        //     console.log(`r:${c24666a.r}`)
        //     get_caller_function(this)
        }
        return result;
    };
    let ryw = Java.use("tb.ryw")
    ryw["a"].overload('java.util.HashMap', 'java.util.HashMap', 'java.lang.String', 'java.lang.String', 'boolean', 'java.lang.String').implementation = function (hashMap, hashMap2, str, str2, z, str3) {
        var api = hashMap.get('api').toString();
        if(api.indexOf('detail') != -1){
            console.log(`run hashMap:${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`)
        }
        let result = this["a"](hashMap, hashMap2, str, str2, z, str3);
        return result;
    };
    /**
     * 获取Response内容(detail走这里) 并send到python 
     */
    // let StreamNetworkCallbackAdapter = Java.use("mtopsdk.mtop.network.StreamNetworkCallbackAdapter");
    // StreamNetworkCallbackAdapter["buildMtopResponse"].implementation = function (c24701b) {
    //     let result = this["buildMtopResponse"](c24701b);
    //     if(result.api.value == 'mtop.taobao.detail.data.get'){
    //         var result_string = result.toString()
    //         // 获取前半部分内容 (此api返回三部分内容)
    //         if(result_string.indexOf('detailabtestdetail') != -1){
    //             send({'body':result_string})
    //         }
    //     }
    //     else{
    //         console.log(result.api.value)
    //         // console.log(result.toString())
    //     }
    //     return result;
    // };

    // StreamNetworkCallbackAdapter.buildMtopResponse.overload('mtopsdk.network.domain.b').implementation = function(bArr){
    //     console.log('\r\n\r\n\r\n\r\n')
    //     // console.log('buidMtopResponse bVar:', bArr)
    //     // var result = this.buildMtopResponse(bArr)
    //     // console.log('mtopresponse.bytedata:', result.bytedata.value)
    //     // console.log('mtopresponse.mtopcontext:', this.mtopContext)
    //     bArr.class.getFields().forEach(function(field){
    //         console.log('field${field}', field)
    //     })
    //     var g_value = bArr.g.value
    //     if(g_value != null){
            
            
    //         console.log('\r\n\r\nbArr.a:', bArr.a.value)    // request headers
    //         console.log('bArr.b:', bArr.b.value)    // 200 状态
    //         console.log('bArr.c:', bArr.c.value)    // 
    //         console.log('bArr.d:', bArr.d.value)    // 

    //         console.log('bArr.e:', bArr.e.value)    // 
    //         console.log('bArr.f:', bArr.f.value)    // 
    //         console.log('bArr.g:', bArr.g.value.length)    // 正常二进制
    //         console.log('bArr.h:', bArr.h.value)    // tb.ryq@a7ae814
    //         // console.log('bArr.i:', bArr.i.value)    // 文本内容
    //         console.log('bArr.j:', bArr.j.value)    // null
    //         console.log('bArr.$ipChange:', bArr.$ipChange)    // 
    //     }
        
    //     return this.buildMtopResponse(bArr)
    // }

    /**
     * 下方是 amdc 模块  猜测是心跳/调度模块
     */
    // let AmdcRuntimeInfo = Java.use("anet.channel.strategy.dispatch.AmdcRuntimeInfo");
    // AmdcRuntimeInfo["setSign"].implementation = function (iAmdcSign) {
    //     console.log(`AmdcRuntimeInfo.setSign is called: iAmdcSign=${iAmdcSign}`);
    //     this["setSign"](iAmdcSign);
    // };

    // let DispatchConstants = Java.use("anet.channel.strategy.dispatch.DispatchConstants");
    // DispatchConstants["isAmdcServerDomain"].implementation = function (str) {
    //     console.log(`DispatchConstants.isAmdcServerDomain is called: str=${str}`);
    //     let result = this["isAmdcServerDomain"](str);
    //     console.log(`DispatchConstants.isAmdcServerDomain result=${result}`);
    //     get_caller_function(this)
    //     return result;
    // };
    // DispatchConstants["setAmdcServerDomain"].implementation = function (strArr) {
    //     console.log(`DispatchConstants.setAmdcServerDomain is called: strArr=${strArr}`);
    //     this["setAmdcServerDomain"](strArr);
    // };

    // let StrategyTable = Java.use("anet.channel.strategy.StrategyTable");
    // StrategyTable["sendAmdcRequest"].overload('boolean', 'java.util.Set', 'boolean', 'boolean').implementation = function (z, set, z2, z3) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: z=${z}, set=${set}, z2=${z2}, z3=${z3}`);
    //     this["sendAmdcRequest"](z, set, z2, z3);
    // };
    // StrategyTable["sendAmdcRequest"].overload('boolean', 'java.util.Set').implementation = function (z, set) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: z=${z}, set=${set}`);
    //     this["sendAmdcRequest"](z, set);
    // };
    // StrategyTable["sendAmdcRequest"].overload('java.util.Set', 'boolean', 'boolean').implementation = function (set, z, z2) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: set=${set}, z=${z}, z2=${z2}`);
    //     this["sendAmdcRequest"](set, z, z2);
    // };
    // StrategyTable["sendAmdcRequest"].overload('java.util.Set').implementation = function (set) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: set=${set}`);
    //     this["sendAmdcRequest"](set);
    // };
    // StrategyTable["sendAmdcRequest"].overload('boolean', 'java.lang.String', 'boolean').implementation = function (z, str, z2) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: z=${z}, str=${str}, z2=${z2}`);
    //     this["sendAmdcRequest"](z, str, z2);
    // };
    // StrategyTable["sendAmdcRequest"].overload('java.lang.String', 'boolean').implementation = function (str, z) {
    //     console.log(`StrategyTable.sendAmdcRequest is called: str=${str}, z=${z}`);
    //     this["sendAmdcRequest"](str, z);
    // };

    // let StrategyResultParser = Java.use("anet.channel.strategy.StrategyResultParser");
    // StrategyResultParser["parse"].implementation = function (jSONObject) {
    //     console.log(`StrategyResultParser.parse is called: jSONObject=${jSONObject}`);
    //     let result = this["parse"](jSONObject);
    //     console.log(`StrategyResultParser.parse result=${result}`);
    //     return result;
    // };

})

/*
GET /gw/mtop.taobao.detail.data.get/1.0/?data=%7B%22detail_v%22%3A%223.3.2%22%2C%22exParams%22%3A%22%7B%5C%22appReqFrom%5C%22%3A%5C%22detail%5C%22%2C%5C%22container_type%5C%22%3A%5C%22xdetail%5C%22%2C%5C%22countryCode%5C%22%3A%5C%22CN%5C%22%2C%5C%22cpuCore%5C%22%3A%5C%226%5C%22%2C%5C%22cpuMaxHz%5C%22%3A%5C%22null%5C%22%2C%5C%22deviceLevel%5C%22%3A%5C%22medium%5C%22%2C%5C%22dinamic_v3%5C%22%3A%5C%22true%5C%22%2C%5C%22dynamicJsonData%5C%22%3A%5C%22true%5C%22%2C%5C%22finalUltron%5C%22%3A%5C%22true%5C%22%2C%5C%22from%5C%22%3A%5C%22shopRec%5C%22%2C%5C%22industryMainPicDegrade%5C%22%3A%5C%22false%5C%22%2C%5C%22isPadDevice%5C%22%3A%5C%22false%5C%22%2C%5C%22item_id%5C%22%3A%5C%22655125762789%5C%22%2C%5C%22latitude%5C%22%3A%5C%220%5C%22%2C%5C%22liveAutoPlay%5C%22%3A%5C%22true%5C%22%2C%5C%22longitude%5C%22%3A%5C%220%5C%22%2C%5C%22newStruct%5C%22%3A%5C%22true%5C%22%2C%5C%22nick%5C%22%3A%5C%22%E9%94%8B%E9%B8%BF%E5%BF%97%E8%BF%9C%5C%22%2C%5C%22openFrom%5C%22%3A%5C%22pagedetail%5C%22%2C%5C%22originalHost%5C%22%3A%5C%22a.m.taobao.com%5C%22%2C%5C%22originalItemId%5C%22%3A%5C%22654837906356%5C%22%2C%5C%22osVersion%5C%22%3A%5C%2232%5C%22%2C%5C%22phoneType%5C%22%3A%5C%222206122SC%5C%22%2C%5C%22pre_item_id%5C%22%3A%5C%22654837906356%5C%22%2C%5C%22preload_v%5C%22%3A%5C%22industry%5C%22%2C%5C%22pvid%5C%22%3A%5C%221a1e0b1b-eb2f-4333-bec7-25697ca62721%5C%22%2C%5C%22scm%5C%22%3A%5C%221007.20777.345540.100200300000019%5C%22%2C%5C%22screenHeight%5C%22%3A%5C%221280%5C%22%2C%5C%22screenWidth%5C%22%3A%5C%22720%5C%22%2C%5C%22soVersion%5C%22%3A%5C%222.0%5C%22%2C%5C%22spm%5C%22%3A%5C%22a2141.7631564.ShopItem%5C%22%2C%5C%22spm-cnt%5C%22%3A%5C%22a2141.7631564%5C%22%2C%5C%22supportIndustryMainPic%5C%22%3A%5C%22true%5C%22%2C%5C%22targetItemId%5C%22%3A%5C%22654837906356%5C%22%2C%5C%22token%5C%22%3A%5C%22759833139%5C%22%2C%5C%22ultron2%5C%22%3A%5C%22true%5C%22%2C%5C%22utdid%5C%22%3A%5C%22ZwzvF2Swb%2FgDAK2RdMwOnx2v%5C%22%2C%5C%22videoAutoPlay%5C%22%3A%5C%22true%5C%22%2C%5C%22xxc%5C%22%3A%5C%22detailRecommend%5C%22%7D%22%2C%22id%22%3A%22655125762789%22%7D HTTP/1.1
 */