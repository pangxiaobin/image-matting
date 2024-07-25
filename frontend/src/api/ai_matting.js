import baseAPI from './base'

export async function aiMattingAPI(action, parameter) {
    return await baseAPI(`ai_matting__${action}`, parameter)
}
