export function construct_query_params(types) {
    let output = '?';
    for (let type in types) {
        if (types[type]) {
            if (output === '?') {
                output += `types=${type}`
            } else {
                output += `&types=${type}`
            }
        }
    }
    return output
}