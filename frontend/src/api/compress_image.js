import baseAPI from './base'

export async function compressImageAPI(action, parameter) {
    return await baseAPI(`compress_image__${action}`, parameter)
}
