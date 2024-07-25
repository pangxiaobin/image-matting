import baseAPI from './base'

export async function settingAPI(action, parameter) {
    return await baseAPI(`setting__${action}`, parameter)
}
