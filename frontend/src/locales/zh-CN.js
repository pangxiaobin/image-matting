export default {
  meta: {
    title: '图像抠图',
    description: '基于AI的图像抠图工具',
  },
  menu: {
    setting: '设置',
    ai_matting_name: 'AI抠图',
  },
  setting: {
    title: '系统设置',
    language: '语言',
    save_dir: '保存路径',
    save_btn: '保存',
    system_info: '系统信息',
    author: '作者',
    version: '版本',
    email: '邮箱',
  },
  ai_matting: {
    btn_back: '返回',
    btn_reselect: '重新选择',
    btn_copy: '复制到剪贴板',
    btn_download: '保存结果',
    copy_success: '复制成功',
    copy_error: '复制失败',
    download_success: '保存成功',
    download_error: '保存失败',
    matting_home: {
      simple_btn: '单张抠图',
      mult_btn: '批量抠图',
      des: '可拖放，粘贴图片或其链接，支持 jpg/png/gif/webp/bmp',
      tips: '试试看',
    },
    mult_matting: {
      title: '批量抠图',
      processing: '进度',
      finish: '结束处理',
    }
  }
};