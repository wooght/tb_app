
/**
 * map 转String
 * @param {*} map 
 * @returns String
 */
export function mapString(map){
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
export function mapKey(map){
    var entrySet = map.entrySet();
    var iterator = entrySet.iterator();
    var map_arr = []
    while (iterator.hasNext()){
        map_arr.push(iterator.next().toString().split('=')[0])
    }
    console.log(`mapKey:${map_arr}`)
    return map_arr
}