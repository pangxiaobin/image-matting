import baseAPI from './base'

export async function aiInpaintingAPI(action, parameter) {
    return await baseAPI(`ai_inpainting__${action}`, parameter)
}
