export default {
  meta: {
    title: 'Image Matting',
    description: 'AI-based image matting tool',
  },
  common: {
    btn_back: 'Back',
    btn_reselect: 'Reselect',
    btn_copy: 'Copy to Clipboard',
    btn_download: 'Save Result',
    copy_success: 'Copied successfully',
    copy_error: 'Copy failed',
    download_success: 'Saved successfully',
    download_error: 'Save failed',
    processing: 'Progress',

  },
  basicHeader: {
    'pin_window': 'Keep Window Always on Top',
    'unpin_window': 'Unpin Window',

  },
  menu: {
    setting: 'Settings',
    about: 'About',
    ai_matting_name: 'AI Matting',
    ai_photo_name: 'ID Photo',
    convert_name: 'Image Conversion',
    compress_name: 'Image Compress',
  },
  setting: {
    title: 'System Settings',
    language: 'Language',
    save_dir: 'Save Path',
    save_btn: 'Save',
    tinify_key: 'TINIFY API Key',
    tinify_used_count: 'Used Count/free 500 per/month',
    tinify_preserving: 'TINIFY Preserving Metadata',
    tinify_preserve_placeholder: 'Select Preserving Metadata',
    
  },
  about: {
    title: 'About',
    desc: 'This is a image matting tool based on deep learning. It can automatically remove the background of images and generate a transparent mask. The tool is powered by PyTorch and OpenCV. The source code is available on GitHub.',
    system_info: 'System Information',
    author: 'Author',
    version: 'Version',
    email: 'Email',
    sponsor: 'Sponsor',
    wx_info: 'WeChat Official Account'
  },
  ai_matting: {
    matting_home: {
      title: 'AI Matting',
      desc: 'Based on AI matting technology, locally run, data secure, easy to use, supports single/batch matting.',
      simple_btn: 'Single Matting',
      mult_btn: 'Batch Matting',
      des: 'Drag and drop, paste image or its link, supports jpg/png/gif/webp/bmp',
      tips: 'Try it out',
    },
    mult_matting: {
      title: 'Batch Matting',
      finish: 'Finish Processing',
    }
  },
  ai_photo: {
    ai_photo_home: {
      title: 'AI ID Photo Maker',
      desc: 'Upload your casual photo, AI will generate an ID photo for you, quickly and easily complete the ID photo making process.',
      tips: 'Support drag and drop, paste to upload',
      upload_btn: 'Upload Photo',
    },
    common_label: 'Common Size',
    common_label_options: {
      option1: '1 inch (295x413)',
      option2: 'Large 1 inch (390x567)',
      option3: 'Small 2 inch (413x531)',
      option4: '2 inch (413x579)',
      option5: '5 inch (1050x1500)',
      option6: '5 inch portrait (1500x1050)',
    },
    id_type_label: 'ID Type',
    id_type_options: {
      option1: 'Civil Servant Review Tool (295x413)',
      option2: 'Civil Servant 34cmx45cm (402x531)',
      option3: 'Civil Servant Small (130x170)',
      option4: 'Civil Servant Small (114x156)',
      option5: 'Judicial Examination (413x626)',
      option6: 'CET/Computer (144x192)',
      option7: 'Accountant (114x156)',
      option8: 'Nurse (160x210)',
      option9: 'Mandarin Test (413x579)',
      option10: 'College Entrance Exam/Postgraduate Entrance Exam (480x640)',
      option11: 'Japanese (360x480)',
      option12: 'ID Card (358x441)',
      option13: 'Social Security Photo (358x441)',
      option14: 'Graduation Certificate (480x640)',
      option15: 'Teacher Qualification Certificate (295x413)',
      option16: 'Passport (390x567)',
      option17: 'Product Image/Avatar (800x800)',
      option18: 'Visa (700x700)',
    },
  },
  convert: {
    convert_home: {
      title: 'Image Conversion Tool',
      desc: 'Convert images to other formats, simple and easy to use, fast conversion, local conversion, data secure.',
      simple_convert_btn: 'Single Conversion',
      mult_convert_btn: 'Batch Conversion',
      tips: 'Supports PNG, JPEG, GIF, BMP, WEBP, ICO, ICNS, TIFF, PDF',

    },
    convert_image: {
      select_btn: 'Select Image',
      convert_btn: 'Convert',
    },
    mult_convert_image: {
      select_folder_btn: 'Select Folder',
      start_convert_btn: 'Start Conversion',
      finish: 'Finish Processing',
    }
  },
  compress: {
    compress_home: {
      title: 'Image Compression Tool',
      desc: 'Compress image size, reduce image quality, and improve loading speed. Uses TinyPNG.com API for compression. API KEY required.',
      simple_compress_btn: 'Single Image Compression',
      mult_compress_btn: 'Batch Compression',
      tips: 'Supports PNG, JPEG, WEBP. Other formats can be converted using a conversion tool before compression.',
    },
    compress_single: {
      select_btn: 'Select Image',
      compress_btn: 'Compress Image',
      original_title: 'Original Image Information',
      compressed_title: 'Compressed Image Information',
      size: 'Size',
      format: 'Format',
      color_mode: 'Color Mode',
      file_size: 'File Size',
      compress_rate: 'Compression Rate',
      path: 'Path',
    },
    mult_compress_image: {
      select_folder_btn: 'Select Folder',
      start_compress_btn: 'Start Compression',
      retry_btn:'Retry Compress',
      finish: 'Finish Processing',
    }
  }
  
};