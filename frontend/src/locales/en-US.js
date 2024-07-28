export default {
  meta: {
    title: 'Image Matting',
    description: 'AI-based image matting tool',
  },
  menu: {
    setting: 'Settings',
    ai_matting_name: 'AI Matting',
    ai_photo_name: 'ID Photo',
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
      simple_btn: 'Single Image Matting',
      mult_btn: 'Batch Matting',
      des: 'You can drag and drop, paste images or their links, supports jpg/png/gif/webp/bmp',
      tips: 'Give it a try',
    },
    mult_matting: {
      title: 'Batch Matting',
      processing: 'Processing',
      finish: 'Finish Processing',
    }
  },
  ai_photo: {
    ai_photo_home: {
      title: 'AI ID Photo Maker',
      desc: 'Upload your casual photo, AI will automatically generate an ID photo, making ID photo creation quick and easy.',
      tips: 'Supports drag and drop, paste upload',
      upload_btn: 'Upload Photo',
    },
    common_label: 'Common Sizes',
    common_label_options: {
      "option1": "1 Inch (295x413)",
      "option2": "Large 1 Inch (390x567)",
      "option3": "Small 2 Inch (413x531)",
      "option4": "2 Inch (413x579)",
      "option5": "5 Inch (1050x1500)",
      "option6": "5 Inch Portrait (1500x1050)"
    },
    id_type_label: 'ID Type',
    id_type_options: {
      "option1": "Civil Service Review Tool (295x413)",
      "option2": "Civil Service 34cmx45cm (402x531)",
      "option3": "Small Civil Service (130x170)",
      "option4": "Small Civil Service (114x156)",
      "option5": "Judicial Exam (413x626)",
      "option6": "CET/Computer (144x192)",
      "option7": "Accounting (114x156)",
      "option8": "Nurse (160x210)",
      "option9": "Mandarin Test (413x579)",
      "option10": "College Entrance Exam/Graduate Exam (480x640)",
      "option11": "Japanese (360x480)",
      "option12": "ID Card (358x441)",
      "option13": "Social Security Photo (358x441)",
      "option14": "Graduation Certificate (480x640)",
      "option15": "Teacher Qualification Certificate (295x413)",
      "option16": "Passport (390x567)",
      "option17": "Product Image/Avatar (800x800)",
      "option18": "Visa (700x700)"
    }
  },
  common: {
    btn_back: 'Back',
    btn_reselect: 'Reselect',
    btn_copy: 'Copy to Clipboard',
    btn_download: 'Save Result',
    copy_success: 'Copy Success',
    copy_error: 'Copy Failed',
    download_success: 'Save Success',
    download_error: 'Save Failed',
  }
};
