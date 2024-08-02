export default {
  meta: {
    title: '图像抠图',
    description: '基于AI的图像抠图工具',
  },
  common: {
    btn_back: '返回',
    btn_reselect: '重新选择',
    btn_copy: '复制到剪贴板',
    btn_download: '保存结果',
    copy_success: '复制成功',
    copy_error: '复制失败',
    download_success: '保存成功',
    download_error: '保存失败',
    processing: '进度',

  },
  menu: {
    setting: '设置',
    ai_matting_name: 'AI抠图',
    ai_photo_name: '证件照',
    convert_name: "图片转换"
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
    matting_home: {
      title: 'AI 抠图',
      desc: '基于 AI 抠图技术、本地运行、数据安全、简单易用、支持单张/批量抠图。',
      simple_btn: '单张抠图',
      mult_btn: '批量抠图',
      des: '可拖放，粘贴图片或其链接，支持 jpg/png/gif/webp/bmp',
      tips: '试试看',
    },
    mult_matting: {
      title: '批量抠图',
      finish: '结束处理',
    }
  },
  ai_photo: {
    ai_photo_home: {
      title: 'AI 证件照制作',
      desc: '上传你的生活照片,AI将自动生成一张证件照,快速、轻松地完成证件照制作。',
      tips: ' 支持拖拽、粘贴上传',
      upload_btn: '上传照片',
    },
    common_label: '常规尺寸',
    common_label_options: {
      "option1": "一寸(295x413)",
      "option2": "大一寸(390x567)",
      "option3": "小二寸(413x531)",
      "option4": "二寸(413x579)",
      "option5": "五寸(1050x1500)",
      "option6": "五寸竖版(1500x1050)"
    },
    id_type_label: '证件类型',
    id_type_options: {
      "option1": "公务员审核工具(295x413)",
      "option2": "公务员34cmx45cm(402x531)",
      "option3": "公务员小(130x170)",
      "option4": "公务员小(114x156)",
      "option5": "司法考试(413x626)",
      "option6": "四六级/计算机(144x192)",
      "option7": "会计(114x156)",
      "option8": "护士(160x210)",
      "option9": "普通话测试(413x579)",
      "option10": "高考/考研(480x640)",
      "option11": "日语(360x480)",
      "option12": "身份证(358x441)",
      "option13": "社保照片(358x441)",
      "option14": "毕业证(480x640)",
      "option15": "教师资格证(295x413)",
      "option16": "护照(390x567)",
      "option17": "产品图/头像(800x800)",
      "option18": "签证(700x700)"
    }

  },
  convert: {
    convert_home: {
      title: '图片转换工具',
      desc: '将图片转换为其他格式，简单易用、快速转换、本地转换、数据安全。',
      simple_convert_btn: '单张转换',
      mult_convert_btn: '批量转换',
      tips: '支持 PNG, JPEG, GIF, BMP, WEBP, ICO, ICNS, TIFF, PDF',

    },
    convert_image: {
      select_btn: '选择图片',
      convert_btn: '转换',
    },
    mult_convert_image: {
      select_folder_btn: '选择文件夹',
      start_convert_btn: '开始转换',
      finish: '结束处理', 
    }
  }
};