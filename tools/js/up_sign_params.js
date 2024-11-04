function call_new_sign(hashMap, hashMap2, str, str2, z, str3){
    var ryw = Java.use("tb.ryw")
    var result_sign
    Java.perform(function(){
        Java.choose('tb.ryw', {
            onMatch: function(instance){
                console.log(`custom run ryw.a: hashMap=${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
                result_sign = instance['a'](hashMap, hashMap2, str, str2, z, str3)
            },
            onComplete:function(){
                console.log('get sign ok')
            }
        })
    })
    return result_sign
}

function get_falcoId(){
    var result = ''
    var FullTraceAnalysis = Java.use("com.taobao.analysis.fulltrace.FullTraceAnalysis");
    Java.perform(function(){
        Java.choose('com.taobao.analysis.fulltrace.FullTraceAnalysis', {
            onMatch: function(instance){
                result = instance['createRequest']('mtop')
                console.log('new falcoId:', result)
            },
            onComplete: function(){
                console.log('get falcoId end')
            }
        });
    });
    return result
}
Java.perform(function () {
    if(Java.available){
        console.log("Android Version:",Java.androidVersion);
    }
    // var ClassName=Java.use("com.luoye.test.ClassName");
    // var instance = ClassName.$new();

    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
        // var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        // console.log('start:' + ret)
        return false;
    };

    var MapH = Java.use('java.util.HashMap')
    // var hm1 = {
    //     "deviceId":"AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF",
    //     "sid"="25601ccd9fad1321ce4f2a5cebbd86dd",
    //     "uid"="4060247732", "x-features"="27", "appKey"="21646297", "api"="mtop.taobao.wireless.home.category", "lat"="39.633542", "lng"="115.109334", "mtopBusiness"=true, "utdid"="Zs7Pnkn0r40DAKSy/CBlF7cX", "extdata"=openappkey=DEFAULT_AUTH, ttid=703304@taobao_android_10.39.10, t=1726655388, v=1.0
    // }
    var sign_params = ''
    var now_time = ''
    var hm = {'data':'', 'deviceId': 'AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF', 'sid': '25601ccd9fad1321ce4f2a5cebbd86dd', 'uid': '4060247732', 'x-features': '27', 'appKey': '21646297', 'api': 'mtop.taobao.wireless.home.category', 'lat': '39.633542', 'lng': '115.109334', 'mtopBusiness': 'true', 'utdid': 'Zs7Pnkn0r40DAKSy/CBlF7cX', "extdata":"openappkey=DEFAULT_AUTH", 'ttid': '703304@taobao_android_10.39.10', 't': '1726655388', 'v': '1.0'}
    var hm2 = {"pageId":"http://m.taobao.com/index.htm", "pageName":"com.taobao.tao.welcome.Welcome"}
    var st = '21646297'
    var st2 = null
    var zz = false
    var st3
    var t
    var result_sign
    var is_set_hm = false
    var hhmm = MapH.$new()
    var hhmm2 = MapH.$new()
    var request_form
    Object.keys(hm).forEach(function(k){
        hhmm.put(k, hm[k])
    })
    hhmm.remove('extdata')
    hhmm.put('extdata', hhmm.get('openappkey'))

    Object.keys(hm2).forEach(function(k){
        hhmm2.put(k, hm2[k])
    })
    console.log(`${hhmm}`)

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
    // function get_new_map(){
    //     Java.cast({'data':123},MapH)
    // }
    let ryw = Java.use("tb.ryw")
    ryw["a"].overload('java.util.HashMap', 'java.util.HashMap', 'java.lang.String', 'java.lang.String', 'boolean', 'java.lang.String').implementation = function (hashMap, hashMap2, str, str2, z, str3) {
        if(hashMap.get('api') == 'mtop.taobao.wireless.home.category'){
            if(!is_set_hm){
                // st = str
                // st2 = str2
                // zz = z
                // st3 = str3
                // hhmm2 = hashMap2
                hhmm.remove('extdata')
                hhmm.put('extdata', hashMap.get('extdata'))
                hhmm.remove('data')
                hhmm.put('data', hashMap.get('data'))
                t = hashMap.get('t').toString()
                console.log(`hashMap.get(data):${hashMap.get('data')}`)
                console.log(`)_)_)_)_)_)()()()()()()()hhmm.get(data):${hhmm.get('data')}`)
                is_set_hm = true
                console.log(`is_set_hm set True${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
            }
        }
        str3 = 'r_31'
        console.log(`ryw.mo140317a is called: hashMap=${hashMap}, hashMap2=${hashMap2}, str=${str}, str2=${str2}, z=${z}, str3=${str3}`);
        let result = this["a"](hashMap, hashMap2, str, str2, z, str3);
        console.log(`ryw.mo140317a result=${result}`);
        // send({'type':'sign','data':`${result}`})
        result_sign = result.toString()
        return result;
    };
    let FullTraceAnalysis = Java.use("com.taobao.analysis.fulltrace.FullTraceAnalysis");
    FullTraceAnalysis['createRequest'].overload('java.lang.String').implementation = function(str){
        var result = this['createRequest'](str)
        var result_2 = this['createRequest'](str)
        console.log('createRequest:', result, result_2)
        return result_2
    }
});