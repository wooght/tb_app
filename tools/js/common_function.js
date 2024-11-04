//export get_caller_function = function(obj){
//    /**
//     * 遍历运行栈队列/栈帖
//     */
//    var current_thread = Java.use('java.lang.Thread').currentThread();
//    var stackTrace = current_thread.getStackTrace();
//    console.log('\n==-==-stack trace start:')
//    stackTrace.forEach(function(stackFrame){
//        console.log(stackFrame.toString())
//    })
//    console.log('\n==-==-stack trace end')
//}
//
//export function get_fields(c){
//    /**
//     * 遍历属性
//     */
//    // c.class.getFields().forEach(function(field){
//    //     console.log('field${field}', c[field.name])
//    // })
//    // return c.class
//    console.log('get_fields run:')
//    Object.keys(c).forEach(function(key){
//        console.log(`${key}:`, c[key].value)
//    })
//}
//
///**
// * 获取hashMap 的key值,返回array
// * @param {*} map
// * @returns
// */
//export function mapKey(map){
//    var entrySet = map.entrySet();
//    var iterator = entrySet.iterator();
//    var map_arr = []
//    while (iterator.hasNext()){
//        map_arr.push(iterator.next().toString().split('=')[0])
//    }
//    return map_arr
//}