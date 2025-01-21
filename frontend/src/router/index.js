import {
  createRouter,
  createWebHashHistory
} from 'vue-router'

const routes = [{
    path: '/',
    component: () => import('@/views/Layout/Layout.vue'),
    children: [{
        path: '',
        component: () => import('@/views/AIMatting/AIMattingHome.vue')
      }, {
        path: 'aimatting',
        name: 'AIMattingHome',
        component: () => import('@/views/AIMatting/AIMattingHome.vue')
      },
      {
        path: 'simple-img',
        name: 'SimpleImg',
        component: () => import('@/views/AIMatting/SimpleImg.vue')
      },
      {
        path: 'multi-img',
        name: 'MultiImg',
        component: () => import('@/views/AIMatting/MulatingImg.vue')
      },
      {
        path: 'ai-photo',
        name: 'AIPhotoHome',
        component: () => import('@/views/AIPhoto/AIPhotoHome.vue')

      }, {
        path: 'image-editor',
        name: 'ImageEditor',
        component: () => import('@/views/AIPhoto/AIPhotoEditor.vue')
      },
      {
        path: 'ai-photo-result',
        name: 'AIPhotoResult',
        component: () => import('@/views/AIPhoto/AIPhotoResult.vue')
      },
      {
        path: 'convert-home',
        name: 'convertImageHome',

        component: () => import('@/views/ConvertImage/ConvertHome.vue')
      },
      {
        path: 'convert-image-editor',
        name: 'ConvertImageEditor',
        component: () => import('@/views/ConvertImage/ConvertImageEditor.vue')
      },
      {
        path: 'multi-convert-image',
        name: 'MultiConvertImage',
        component: () => import('@/views/ConvertImage/MultiConvertImage.vue')
      }, 
      {
        path: 'compress-home',
        name: 'CompressHome',
        component: () => import('@/views/CompressImage/CompressHome.vue')
      }, 
      {
        path: 'comporess-single',
        name: 'CompressSingle',
        component: () => import('@/views/CompressImage/CompressSingle.vue')
      }, 
      {
        path: 'compress-multi',
        name: 'CompressMulti',
        component: () => import('@/views/CompressImage/CompressMulti.vue')
      },
      {
        path: 'setting',
        name: 'Setting',
        component: () => import('@/views/Setting.vue')
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('@/views/About.vue')
      },
      {
        path: '/ai-inpainting',
        name: 'AIInpaintingHome',
        component: () => import('@/views/AIInpainting/AIInpaintingHome.vue')
      },
      {
        path: '/ai-inpainting/editor',
        name: 'AIInpaintingEditor', 
        component: () => import('@/views/AIInpainting/AIInpaintingEditor.vue')
      }

    ]
  }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router