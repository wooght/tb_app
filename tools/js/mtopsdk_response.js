function echo(t){
    console.log(t)
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
function get_caller_function(obj){
    /**
     * 遍历运行栈队列/栈帖
     */
    var current_thread = Java.use('java.lang.Thread').currentThread();
    var stackTrace = current_thread.getStackTrace();
    echo('\n==-==-stack trace start:')
    stackTrace.forEach(function(stackFrame){
        console.log(stackFrame.toString())
    })
    echo('\n==-==-stack trace end')
}
function mapToString(hash_map) {
    var result = "";
    var keyset = hash_map.keySet();
    var it = keyset.iterator();
    while (it.hasNext()) {
        var keystr = it.next().toString();
        var valuestr = hash_map.get(keystr).toString();
        result += keystr +"="+valuestr+"&";
    }
    return result.substring(0, result.length - 1);
}
function mapString(map){
    var entrySet = map.entrySet();
    var iterator = entrySet.iterator();
    while (iterator.hasNext()){
        console.log(iterator.next())
    }
}

Java.perform(function(){
    // android 版本
    if(Java.available){
        console.log("Android Version:",Java.androidVersion);
    }
    // 关闭spdy协议
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function(){
        // var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        // console.log('start:' + ret)
        return false;
    };

    /**
     * response 内容
     */
    // 获取response的headers
    let MtopResponse = Java.use("mtopsdk.mtop.domain.MtopResponse");
    MtopResponse["setHeaderFields"].implementation = function(map){
        // console.log(`\nMtopResponse.setHeaderFields is called: map=${map}`);
        // mapString(map)                           // response headers内容
        // get_caller_function(this)
        this["setHeaderFields"](map);
    };
    // MtopResponse["getRetMsg"].implementation = function () {
    //     console.log(`MtopResponse.getRetMsg is called`);
    //     let result = this["getRetMsg"]();       // 获取返回结果 如:调用成功
    //     console.log(`MtopResponse.getRetMsg result=${result}`);
    //     return result;
    // };
    // 获取response结果
    // let MtopFinishEvent = Java.use("mtopsdk.mtop.common.MtopFinishEvent");
    // MtopFinishEvent["getMtopResponse"].implementation = function () {
    //     console.log(`MtopFinishEvent.getMtopResponse is called`);
    //     let result = this["getMtopResponse"]();
    //     console.log(`MtopFinishEvent.getMtopResponse result=${result}`);
    //     return result;
    // };

    /**
     * request 内容
     */
    // 获取request的内容
    // let MtopRequest = Java.use("mtopsdk.mtop.domain.MtopRequest");
    // MtopRequest["getData"].implementation = function () {
    //     // console.log(`MtopRequest.getData is called`);
    //     let result = this["getData"]();
    //     console.log('===> API:', this['getApiName']())       // 获取API名称
    //     // console.log(`MtopRequest.getData result=${result}`);
    //     return result;
    // };
    let ApiID = Java.use("mtopsdk.mtop.common.ApiID");
    // c24666a 为MTOP request的部分,不包括cookie,也只有部分headers
    // ApiID["$init"].implementation = function (rynVar, c24666a) {
    //     console.log(`ApiID.$init is called: rynVar=${rynVar}, c24666a=${c24666a}`);
    //     get_fields(c24666a)
    //     echo(c24666a.a.value)               // undefined
    //     // echo(c24666a.b.value)               // MtopRequest 内容
    //     echo(`c:${c24666a.c.value}`)               // null
    //     echo(c24666a.d.value.toString())    //   method=POST henaders的一部分
    //     echo(`params e:${c24666a.e.value.toString()}`)               // MtopListener
    //     echo(`f:${c24666a.f.value}`)
    //     echo(`g:${c24666a.g.value}`)
    //     echo(`h:${c24666a.h.value}`)        // MTOP233  应该是请求次数
    //     echo(`i:${c24666a.i.value}`)
    //     echo(`j:${c24666a.j.value}`)
    //     echo(`k:${c24666a.k.value}`)
    //     echo(`l:${c24666a.l.value}`)        // null
    //     echo(`m:${c24666a.m.value}`)
    //     echo(`n:${c24666a.n.value}`)        // null
    //     echo(`o:${c24666a.o.value}`)        // MtopBuilder  com.taobao.tao.remotebusiness.RemoteBusiness@77d83d9
    //     echo(`p:${c24666a.p.value}`)        // 0
    //     this["$init"](rynVar, c24666a);
    // };
    // 有reques theaders 函数,但没有发挥作用

    /**
     * 调用顺序:MtopBuilder->convert->setRequestHeaders->rye 
     * */ 
    // 创建request headers, 返回的是headers内容,无cookie
    let AbstractNetworkConverter = Java.use("mtopsdk.mtop.protocol.converter.impl.AbstractNetworkConverter");
    // AbstractNetworkConverter["buildRequestHeaders"].implementation = function (map, map2, z) {
    //     console.log(`AbstractNetworkConverter.buildRequestHeaders is called: map=${map}, map2=${map2}, z=${z}`);
    //     let result = this["buildRequestHeaders"](map, map2, z);
    //     console.log(`AbstractNetworkConverter.buildRequestHeaders result=${result}`);
    //     console.log(mapString(result))
    //     return result;
    // };

    // let rxy = Java.use("tb.rxy");
    // rxy["b"].implementation = function (c24666a) {
    //     console.log(`rxy.mo140277b is called: c24666a=${c24666a}`);
    //     let result = this["b"](c24666a);
    //     console.log(`rxy.mo140277b result=${c24666a}`);
    //     get_fields(c24666a)
    //     return result;
    // };

    /**
     * 
     * @param {*} r27 
     * @returns 进程栈
     * mtopsdk.mtop.protocol.converter.impl.AbstractNetworkConverter.convert(Native Method)
        tb.rxy.b(Taobao:40)
        tb.ryj.a(Taobao:60)
        mtopsdk.mtop.intf.MtopBuilder.asyncRequest(Taobao:941)
        mtopsdk.mtop.intf.MtopBuilder.asyncRequest(Taobao:957)
        com.taobao.tao.remotebusiness.MtopBusiness.startRequest(Taobao:292)
        com.taobao.tao.remotebusiness.MtopBusiness.startRequest(Taobao:242)
        com.taobao.android.ucp.bridge.NativeDelegate$8.callback(Taobao:345)
        com.taobao.android.ucp.bridge.NativeBroadcast.sendMessage(Taobao:224)
     */

    // 返回Request,{method=POST, appKey=21646297, headers={}, api=,..} 这里参数r27为C24666a
    // AbstractNetworkConverter["convert"].implementation = function (r27) {
    //     console.log(`AbstractNetworkConverter.convert is called: null=${r27}`);
    //     let result = this["convert"](r27);
    //     console.log(`---->AbstractNetworkConverter.convert result=${result}`);
    //     console.log(`\n c:${r27.c.value}`)     // null  本应该是返回内容,这里还没有
    //     // console.log(`b:${r27.b.value}`)     // 提交内容
    //     // console.log(`a:${result.a}`)
    //     // console.log(`b:${result.b}`)        // POST
    //     // mapString(result.c.value)           // c 为 headers
    //     // console.log(`d:${result.d}`)
    //     // console.log(`e:${result.e}`)
    //     // console.log(`f:${result.f}`)
    //     // console.log(`g:${result.g}`)
    //     // console.log(`h:${result.h}`)
    //     // console.log(`i:${result.i}`)
    //     // console.log(`j:${result.j}`)
    //     // console.log(`k:${result.k}`)
    //     // console.log(`l:${result.l}`)
    //     // console.log(`m:${result.m}`)
    //     // console.log(`n:${result.n}`)
    //     // console.log(`o:${result.o}`)
    //     // console.log(`p:${result.p}`)
    //     // console.log(`q:${result.q}`)
    //     console.log(`r:${result.r}`)        // api  value: mtop.taobao.wireless.home.category
    //     // console.log(`s:${result.s}`)        // null
    //     // console.log(`t:${result.t}`)        // null
    //     // console.log(`y:${result.y}`)
    //     get_caller_function()
    //     return result;
    // };


    // 返回headers 字符串
    // let Request = Java.use("mtopsdk.network.domain.Request");
    // Request["toString"].implementation = function () {
    //     console.log(`Request.toString is called`);
    //     let result = this["toString"]();
    //     console.log(`Request.toString result=${result}`);
    //     return result;
    // };

    // 开始构建Request
    // let MtopBuilder = Java.use("mtopsdk.mtop.intf.MtopBuilder");
    // MtopBuilder["asyncRequest"].overload().implementation = function () {
    //     console.log(`MtopBuilder.asyncRequest is called`);
    //     let result = this["asyncRequest"]();
    //     console.log(`MtopBuilder.asyncRequest result=${result}`);
    //     console.log(result)      // tb.ryn
    //     return result;
    // };


    /**
     * c24666a类,包含response,request内容
     * 进程栈:
     * dalvik.system.VMStack.getThreadStackTrace(Native Method)
        java.lang.Thread.getStackTrace(Thread.java:1724)
        tb.rye.a(Native Method)
        tb.ryj.b(Taobao:96)
        mtopsdk.mtop.network.NetworkCallbackAdapter$1.run(Taobao:110)
        java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:462)
        java.util.concurrent.FutureTask.run(FutureTask.java:266)
        java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
        java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
        java.lang.Thread.run(Thread.java:920)
        mtopsdk.mtop.util.MtopSDKThreadPoolExecutorFactory$MtopSDKThreadFactory$1.run(Taobao:80)
     */
    let rye = Java.use("tb.rye");
    rye["a"].overload('mtopsdk.framework.domain.a').implementation = function (c24666a) {
        console.log(`\nrye.mo140276a is called: c24666a=${c24666a}`);

        if(c24666a.l.value == 'https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.newface.awesome.get/1.0/'){
            echo(c24666a.a.value)               // undefined
            // echo(`b:${c24666a.b.value}`)        // MtopRequest 提交内容 [apiName=string, data={}, version=string] 用法:c24666a.b.getApiName()
             echo(`c Response Body:${c24666a.c.value}`)        // 请求成功,response 返回内容
            // echo(c24666a.d.value.toString())    //   MtopNetworkProp henaders的一部分
            echo(`params e:${get_fields(c24666a.e.value)}`)               // MtopListener
            // echo(`f:${c24666a.f.value}`)        // apiid
            // echo(`g:${c24666a.g.value}`)        // MtopStatistics 79918752[SumStat(ms)]
            // echo(`h:${c24666a.h.value}`)        // MTOP233  应该是请求次数
            echo(`i Request POST:${mapToString(c24666a.i.value)}`)        // request data POST提交内容
            // echo(`j:${c24666a.j.value}`)        // null
            echo(`k Request Headers:${c24666a.k.value}`)        // Request headers
            // mapString(c24666a.k.value.c.value)
            echo(c24666a.k.value.r.value)

            echo(`l:${c24666a.l.value}`)        // 请求地址
            // echo(`m:${c24666a.m.value}`)        // detail api 中 .data为 提交内容
            // echo(`n:${c24666a.n.value}`)        // Response headers
            // echo(`o:${c24666a.o.value}`)        // MtopBuilder  com.taobao.tao.remotebusiness.RemoteBusiness@77d83d9
            // echo(`p:${c24666a.p.value}`)        // 2311
            echo(`r:${c24666a.r.value}`)
            // get_caller_function(this)
        }
        let result = this["a"](c24666a);
        console.log(`rye.mo140276a result=${result}`, '**********');
        return result;
    };
    // let MtopListener = Java.use("com.alibaba.ability.impl.mtop.MtopAbility$MtopListener");
    // MtopListener["$init"].implementation = function (mtopBusiness, mtopRequest, callback, param, abilityContext) {
    //     console.log(`MtopListener.$init is called: mtopBusiness=${mtopBusiness}, mtopRequest=${mtopRequest}, callback=${callback}, param=${param}, abilityContext=${abilityContext}`);
    //     this["$init"](mtopBusiness, mtopRequest, callback, param, abilityContext);
    // };



    // let MtopBusiness = Java.use("com.taobao.tao.remotebusiness.MtopBusiness");
    // MtopBusiness["startRequest"].overload('int', 'java.lang.Class').implementation = function (i, cls) {
    //     console.log(`MtopBusiness.startRequest is called: i=${i}, cls=${cls}`);
    //     this["startRequest"](i, cls);
    //     console.log(this.apiID)     // value: ApiID [call=mtopsdk.network.impl.b@b9ff5a, mtopContext=mtopsdk.framework.domain.a@5a5116f]
    //     let context = this.apiID.value.mtopContext.value
    //     console.log(get_fields(context.e))
    //     console.log('\n***********************')
    //     // get_fields(context._a.value)
    // };

    /**
     * 估计为发起Request的地方
     */
    // let C24705b = Java.use("mtopsdk.network.impl.b");
    // C24705b["$init"].implementation = function (request, context) {
    //     // console.log(`C24705b.$init is called: request=${request}, context=${context}`);
    //     // console.log(`context:${get_fields(context)}`)
    //     this["$init"](request, context);
    //     get_fields(request)
    //     // console.log(mapString(request.c.value))     // Request headers
    //     console.log(mapString(request.t.value))
    // };

    /**
     * callback
     */
    // let NetworkCallbackAdapter = Java.use("mtopsdk.mtop.network.NetworkCallbackAdapter");
    // NetworkCallbackAdapter["$init"].implementation = function (c24666a) {
    //     console.log(`NetworkCallbackAdapter.$init is called: c24666a=${c24666a}`);
    //     this["$init"](c24666a);
    //     console.log(c24666a.r.value)
    //     console.log(c24666a.j.value)
    //     console.log(c24666a.m.value)
    // };
    // c24701b:Response
    // NetworkCallbackAdapter["onHeader"].overload('mtopsdk.network.domain.b', 'java.lang.Object').implementation = function (c24701b, obj) {
    //     console.log(`NetworkCallbackAdapter.onHeader is called: c24701b=${c24701b}, obj=${obj}`);
    //     this["onHeader"](c24701b, obj);
    // };



    /**
     * cookie 设置相关
     */
    let CookieManager = Java.use("anetwork.channel.cookie.CookieManager");
    CookieManager["setCookie"].overload('java.lang.String', 'java.lang.String', 'java.util.Map').implementation = function (str, str2, map) {
        // console.log(`CookieManager.setCookie is called: str=${str}, str2=${str2}, map=${map}`);
        this["setCookie"](str, str2, map);
    };
    // 验证后设置cookie:x5sec, 其中str为一个网址,时一个json str2是x5sec/sca
    // CookieManager.setCookie(str, str2) is called: str=https://gm.mmstat.com/fsp.1.1?code=15&msg=report%20success%3B&pid=sufeiPunish&page=https%3A%2F%2Ftrade-acs.m.taobao.com%2F%2Fgw%2Fmtop.taobao.detail.data.get%2F1.0%2F_____tmd_____%2Fpunish&query=x5secdata%3Dxd229d016a87ee11fb908f49e67b1ed33b7f2fe6f80ad85ad31728209389a-717315356a-1467249453abaac3bk4060247732fscene__bx__trade-acs.m.taobao.com%253A443%252Fgw%252Fmtop.taobao.detail.data.get%252F1.0%26x5step%3D2%26tmd_nc%3D1%26http_referer%3Dhttps%3A%2F%2Fsec.taobao1111.com%2F&hash=&referrer=&title=%E9%AA%8C%E8%AF%81%E7%A0%81%E6%8B%A6%E6%88%AA&ua=Mozilla%2F5.0%20(Linux%3B%20U%3B%20Android%2012%3B%20zh-CN%3B%202206122SC%20Build%2FV417IR)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Version%2F4.0%20Chrome%2F100.0.4896.58%20UWS%2F5.12.4.0%20Mobile%20Safari%2F537.36%20AliApp(TB%2F10.39.10)%20UCBS%2F2.11.1.1%20TTID%2F703304%40taobao_android_10.39.10%20WindVane%2F8.5.0&c1=908f49e67b1ed33b7f2fe6f80ad85ad3&c2=X82Y__4efeef942d19c56bafab18ba3da969f4&c3=undefined, str2=sca=99070104; path=/; domain=.mmstat.com; SameSite=none; Secure
    CookieManager["setCookie"].overload('java.lang.String', 'java.lang.String').implementation = function (str, str2) {
        console.log(`\nCookieManager.setCookie(str, str2) is called: str=${str}, str2=${str2}\n`);
        this["setCookie"](str, str2);
    };
    CookieManager["setCookie"].overload('java.lang.String', 'java.util.Map').implementation = function (str, map) {
        console.log(`CookieManager.setCookie is called: str=${str}, map=${map}`);
        this["setCookie"](str, map);
    };
    let NetworkSdkSetting = Java.use("anetwork.channel.http.NetworkSdkSetting");
    NetworkSdkSetting["initAsyncConfig"].implementation = function (context2) {
        console.log(`NetworkSdkSetting.initAsyncConfig is called: context2=${context2}`);
        this["initAsyncConfig"](context2);
    };
    NetworkSdkSetting["initAsync"].implementation = function (context2) {
        // console.log(`NetworkSdkSetting.initAsync is called: context2=${context2}`);
        this["initAsync"](context2);
    };
    let sci = Java.use("tb.sci");
    sci["a"].overload('android.content.Context').implementation = function (context) {
        console.log(`sci.m140576a is called: context=${context}`);
        this["a"](context);
    };
    let UploadFileServiceImpl = Java.use("mtopsdk.mtop.upload.service.UploadFileServiceImpl");
    UploadFileServiceImpl["computeUploadToken"].implementation = function (uploadFileInfo, fileBaseInfo) {
        console.log(`UploadFileServiceImpl.computeUploadToken is called: uploadFileInfo=${uploadFileInfo}, fileBaseInfo=${fileBaseInfo}`);
        let result = this["computeUploadToken"](uploadFileInfo, fileBaseInfo);
        console.log(`UploadFileServiceImpl.computeUploadToken result=${result}`);
        return result;
    };

    let LoginDataHelperTask = Java.use("com.ali.user.mobile.base.helper.LoginDataHelperTask");
    LoginDataHelperTask["addCookie2SidCompare"].implementation = function () {
        console.log(`LoginDataHelperTask.addCookie2SidCompare is called`);
        this["addCookie2SidCompare"]();
    };

    /***
     * 获取到的cookie
     */
    // 参数 map 是response的headers
    // CookieManager["setCookie"].overload('java.lang.String', 'java.lang.String', 'java.util.Map').implementation = function (str, str2, map) {
    //     console.log(`-=-=-=-=-=-=-=-=-=-=-=CookieManager.setCookie is called: str=${str}, str2=${str2}, map=${map}`);
    //     this["setCookie"](str, str2, map);
    //     // console.log(mapString(map))
    // };

    // // result 为Request要传递的cookie
    // CookieManager["getCookie"].implementation = function (str) {
    //     console.log(`CookieManager.getCookie is called: str=${str}`);
    //     let result = this["getCookie"](str);
    //     console.log(`CookieManager.getCookie result=${result}`);
    //     return result;
    // };

    // let MtopBuilder = Java.use("mtopsdk.mtop.intf.MtopBuilder");
    // MtopBuilder["asyncRequest"].overload('mtopsdk.mtop.common.MtopListener').implementation = function (mtopListener) {
    //     console.log(`MtopBuilder.asyncRequest is called: mtopListener=${mtopListener}`);
    //     echo(mtopListener.$className)       // $Proxy14 ?
    //     echo(typeof mtopListener)
    //     console.log('fields:', mtopListener.class.getFields())
    //     let result = this["asyncRequest"](mtopListener);
    //     console.log(`MtopBuilder.asyncRequest result=${result}`);
    //     return result;
    // };

    // MtopBuilder["asyncRequest"].overload('mtopsdk.mtop.common.MtopListener').implementation = function (mtopListener) {
    //     console.log(`MtopBuilder.asyncRequest is called: mtopListener=${mtopListener}`);
    //     echo(`this.fullTraceId:${this.fullTraceId}`)
    //     echo('mtopListerner fields:')
    //     echo(mtopListener.class)
    //     get_fields(mtopListener)                // ? 看不到字段
    //     echo('mtopListerner fields end;')
    //     let result = this["asyncRequest"](mtopListener);
    //     get_fields(result.mtopContext.value.k.value)
    //     echo(`result:${result}`)
    //     get_fields(result)
    //     return result;
    // };

    /**
     * 获取UserId
     */
    let NetworkPropertyServiceImpl = Java.use("mtopsdk.mtop.network.NetworkPropertyServiceImpl");
    // NetworkPropertyServiceImpl["setUserId"].implementation = function (str) {
    //     console.log(`NetworkPropertyServiceImpl.setUserId is called: str=${str}`);   // str 为UserId
    //     this["setUserId"](str);
    // };
});