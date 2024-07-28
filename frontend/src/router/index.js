import {
  createRouter,
  createWebHashHistory
} from 'vue-router'

const routes = [{
    path: '/',
    component: () => import('@/views/Layout/Layout.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/AIMatting/AIMattingHome.vue')
      },{
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
        
      },{
        path: 'image-editor',
        name: 'ImageEditor',
        component: () => import('@/views/AIPhoto/ImageEditor.vue')
      },
      {
        path: 'ai-photo-result',
        name: 'AIPhotoResult',
        component: () => import('@/views/AIPhoto/AIPhotoResult.vue')
      },
      {
        path: 'setting',
        name: 'Setting',
        component: () => import('@/views/Setting.vue')
      },
      
    ]
  }

]

const router = createRouter({
  history:createWebHashHistory(),
  routes,
})

export default router