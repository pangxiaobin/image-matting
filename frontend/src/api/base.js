
export default async function baseAPI(path, parameter) {
    if (!window.pywebview) {
        await new Promise(resolve => setTimeout(resolve, 100))
    }
    return JSON.parse(await window.pywebview.api[path](parameter));
}