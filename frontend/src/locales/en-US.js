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
  },
  menu: {
    setting: 'Settings',
    ai_matting_name: 'AI Matting',
    ai_photo_name: 'ID Photo',
    convert_name: 'Image Conversion',
  },
  setting: {
    title: 'System Settings',
    language: 'Language',
    save_dir: 'Save Path',
    save_btn: 'Save',
    system_info: 'System Information',
    author: 'Author',
    version: 'Version',
    email: 'Email',
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
      processing: 'Progress',
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
  }
};