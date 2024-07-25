export default {
  meta: {
    title: 'Image Matting',
    description: 'AI-based image matting tool',
  },
  menu: {
    setting: 'Settings',
    ai_matting_name: 'AI Matting',
  },
  setting: {
    title: 'System Settings',
    language: 'Language',
    save_dir: 'Save Directory',
    save_btn: 'Save',
    system_info: 'System Information',
    author: 'Author',
    version: 'Version',
    email: 'Email',
  },
  ai_matting: {
    btn_back: 'Back',
    btn_reselect: 'Reselect',
    btn_copy: 'Copy to Clipboard',
    btn_download: 'Save Result',
    copy_success: 'Copy Successful',
    copy_error: 'Copy Failed',
    download_success: 'Save Successful',
    download_error: 'Save Failed',
    matting_home: {
      simple_btn: 'Single Image Matting',
      mult_btn: 'Batch Matting',
      des: 'Drag and drop, paste images or their links, supports jpg/png/gif/webp/bmp',
      tips: 'Give it a try',
    },
    mult_matting: {
      title: 'Batch Matting',
      processing: 'Processing',
      finish: 'Processing Finished',
    }
  }
};