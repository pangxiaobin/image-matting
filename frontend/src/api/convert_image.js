import baseAPI from './base'

export async function convertImageAPI(action, parameter) {
    return await baseAPI(`convert_image__${action}`, parameter)
}
