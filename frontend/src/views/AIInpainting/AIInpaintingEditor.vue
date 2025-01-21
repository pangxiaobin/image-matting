<template>
  <div class="editor h-full flex flex-col items-center overflow-hidden">
    <div class="canvas-wrapper relative w-full flex-1 flex items-center justify-center">
      <div class="canvas-container relative" 
           @mouseleave="handleMouseLeave"
           @mouseenter="showBrushPreview = true">
        <canvas ref="imageCanvas" class="base-canvas"></canvas>
        <canvas ref="maskCanvas" class="mask-canvas"
          @mousedown="startDrawing"
          @mousemove="handleMouseMove"
          @mouseup="stopDrawing"
          @mouseleave="stopDrawing"
        ></canvas>
        <!-- 画笔预览 -->
        <div v-if="showBrushPreview" 
          class="eraser-cursor"
          :style="{
            width: `${brushSize}px`,
            height: `${brushSize}px`,
            left: `${cursorX}px`,
            top: `${cursorY}px`,
            backgroundColor: 'rgba(255, 0, 0, 0.1)'
          }">
        </div>
      </div>
    </div>
    <!-- 工具栏 -->
    <div class="toolbar-wrapper mt-4 mb-4">
      <div class="toolbar">
        <div class="flex items-center space-x-4">
          <!-- 画笔大小 -->
          <div class="flex items-center">
            <input type="range" v-model="brushSize" min="1" max="200" class="range range-sm w-32">
            <span class="ml-2 text-white">{{ brushSize }}</span>
          </div>
          
          <!-- 操作按钮 -->
          <button @click="reselectImage" class="toolbar__button" title="Reselect">
            <i class="fa fa-folder-open"></i>
          </button>
          <button @click="undo" class="toolbar__button" title="Undo (Ctrl/Cmd+Z)">
            <i class="fa fa-undo"></i>
          </button>
          <button @click="redo" class="toolbar__button" title="Redo (Ctrl/Cmd+Y)">
            <i class="fa fa-redo"></i>
          </button>
          <button @click="clearMask" class="toolbar__button" title="Clear">
            <i class="fa fa-trash"></i>
          </button>
          <button @click="processImage" class="toolbar__button" :disabled="loading" title="Process">
            <span v-if="!loading"><i class="fa-solid fa-circle-check"></i></span>
            <span v-else class="loading loading-spinner loading-sm"></span>
          </button>
          <button @click="downloadImage" class="toolbar__button" title="Download (Ctrl/Cmd+S)">
            <i class="fa fa-download"></i>
          </button>
         
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="loader"></div>
    </div>
   

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { aiInpaintingAPI } from '@/api/ai_inpainting';
import baseAPI from '@/api/base';
import message from '@/utils/message';

const { t } = useI18n();
const route = useRoute();

// 基础状态
const imageCanvas = ref(null);
const maskCanvas = ref(null);
const originalImage = ref(null);
const loading = ref(false);

// 画笔相关状态
const brushSize = ref(40);
const isDrawing = ref(false);
const showBrushPreview = ref(false);
const cursorX = ref(0);
const cursorY = ref(0);

// 历史记录
const history = ref([]);
const historyIndex = ref(-1);
const imageHistory = ref([]);

// 添加新的状态来保存原始尺寸
const originalWidth = ref(0);
const originalHeight = ref(0);

// 初始化图片
const initImage = async () => {
  loading.value = true;
  try {
    const filePath = route.query.filePath;
    const imgType = route.query.imgType;
    
    let imageUrl = '';
    if (imgType === 'local') {
      const result = await baseAPI('get_local_file_base64', filePath);
      if (result.code === 200) {
        imageUrl = result.data.base64_image;
      }
    } else {
      imageUrl = filePath;
    }

    if (imageUrl) {
      const img = new Image();
      img.onload = () => initCanvas(img);
      img.src = imageUrl;
    }
  } catch (error) {
    message.error('Failed to load image');
  } finally {
    loading.value = false;
  }
};

// 初始化画布
const initCanvas = (img) => {
  if (!img || !imageCanvas.value || !maskCanvas.value) return;

  originalImage.value = img;
  originalWidth.value = img.width;
  originalHeight.value = img.height;
  
  // 计算画布大小
  const maxWidth = 700;
  const maxHeight = 500;
  const scale = Math.min(maxWidth / img.width, maxHeight / img.height);
  const width = img.width * scale;
  const height = img.height * scale;

  // 设置画布尺寸
  [imageCanvas.value, maskCanvas.value].forEach(canvas => {
    canvas.width = width;
    canvas.height = height;
    // 设置更好的图像渲染质量
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
  });

  // 绘制原始图像
  renderImage(img);
  
  // 设置遮罩画布样式
  const maskCtx = maskCanvas.value.getContext('2d');
  maskCtx.fillStyle = 'rgba(255, 0, 0, 0.5)';
  
  saveState();
};

// 鼠标事件处理
const handleMouseMove = (event) => {
  updateCursor(event);
  if (isDrawing.value) {
    draw(event);
  }
};

const updateCursor = (event) => {
  const rect = event.target.getBoundingClientRect();
  cursorX.value = event.clientX - rect.left;
  cursorY.value = event.clientY - rect.top;
};

const handleMouseLeave = () => {
  showBrushPreview.value = false;
  stopDrawing();
};

// 绘制相关函数
const startDrawing = (event) => {
  isDrawing.value = true;
  draw(event);
};

const draw = (event) => {
  const ctx = maskCanvas.value.getContext('2d');
  const rect = event.target.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  ctx.beginPath();
  ctx.arc(x, y, brushSize.value/2, 0, Math.PI * 2);
  ctx.fill();
};

const stopDrawing = () => {
  if (isDrawing.value) {
    isDrawing.value = false;
    saveState();
  }
};

// 历史记录相关
const saveState = () => {
  // 保存遮罩状态
  const maskData = maskCanvas.value.getContext('2d').getImageData(
    0, 0, maskCanvas.value.width, maskCanvas.value.height
  );
  // 保存图像状态
  const imageData = imageCanvas.value.getContext('2d').getImageData(
    0, 0, imageCanvas.value.width, imageCanvas.value.height
  );
  
  // 清除当前位置之后的历史
  history.value = history.value.slice(0, historyIndex.value + 1);
  imageHistory.value = imageHistory.value.slice(0, historyIndex.value + 1);
  
  // 添加新状态
  history.value.push(maskData);
  imageHistory.value.push(imageData);
  historyIndex.value++;
};

const undo = () => {
  if (historyIndex.value > 0) {
    historyIndex.value--;
    const maskCtx = maskCanvas.value.getContext('2d');
    const imageCtx = imageCanvas.value.getContext('2d');
    
    maskCtx.putImageData(history.value[historyIndex.value], 0, 0);
    imageCtx.putImageData(imageHistory.value[historyIndex.value], 0, 0);
  }
};

// 添加 redo 函数
const redo = () => {
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++;
    const maskCtx = maskCanvas.value.getContext('2d');
    const imageCtx = imageCanvas.value.getContext('2d');
    
    maskCtx.putImageData(history.value[historyIndex.value], 0, 0);
    imageCtx.putImageData(imageHistory.value[historyIndex.value], 0, 0);
  }
};

// 图像处理相关
const renderImage = (img) => {
  const ctx = imageCanvas.value.getContext('2d');
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.clearRect(0, 0, imageCanvas.value.width, imageCanvas.value.height);
  ctx.drawImage(img, 0, 0, imageCanvas.value.width, imageCanvas.value.height);
};

const clearMask = () => {
  const ctx = maskCanvas.value.getContext('2d');
  ctx.clearRect(0, 0, maskCanvas.value.width, maskCanvas.value.height);
  saveState();
};

const restoreOriginal = () => {
  if (originalImage.value) {
    renderImage(originalImage.value);
    clearMask();
  }
};

// API相关函数
const processImage = async () => {
  loading.value = true;
  try {
    // 创建临时画布以输出原始尺寸的遮罩
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = originalWidth.value;
    tempCanvas.height = originalHeight.value;
    const tempCtx = tempCanvas.getContext('2d');
    
    // 设置更好的图像渲染质量
    tempCtx.imageSmoothingEnabled = true;
    tempCtx.imageSmoothingQuality = 'high';
    
    // 将当前遮罩缩放到原始尺寸
    tempCtx.drawImage(
      maskCanvas.value,
      0, 0, maskCanvas.value.width, maskCanvas.value.height,
      0, 0, originalWidth.value, originalHeight.value
    );

    const result = await aiInpaintingAPI('inpainting', {
      origin_base64: originalImage.value.src,
      mask_base64: tempCanvas.toDataURL('image/png', 1.0) // 使用最高质量的PNG
    });
    
    if (result.code === 200) {
      const img = new Image();
      img.onload = () => {
        originalImage.value = img;
        renderImage(img);
        clearMask();
        saveState();
        message.success(t('common.processing_success'));
      };
      img.src = result.data.result_base64;
    }
  } catch (error) {
    message.error('Processing failed');
  } finally {
    loading.value = false;
  }
};

const downloadImage = async () => {
  try {
    // 创建临时画布以输出原始尺寸的图像
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = originalWidth.value;
    tempCanvas.height = originalHeight.value;
    const tempCtx = tempCanvas.getContext('2d');
    
    // 设置更好的图像渲染质量
    tempCtx.imageSmoothingEnabled = true;
    tempCtx.imageSmoothingQuality = 'high';
    
    // 将当前图像缩放到原始尺寸
    tempCtx.drawImage(
      imageCanvas.value,
      0, 0, imageCanvas.value.width, imageCanvas.value.height,
      0, 0, originalWidth.value, originalHeight.value
    );

    const response = await baseAPI('save_png_dialog', {
      png_data: tempCanvas.toDataURL('image/png', 1.0), // 使用最高质量的PNG
      origin_data: originalImage.value.src
    });
    
    if (response.code === 200) {
      message.success(t('common.download_success'));
    }
  } catch (error) {
    message.error(t('common.download_error'));
  }
};

// 添加重新选择图片函数
const reselectImage = async () => {
  loading.value = true;
  try {
    const res = await baseAPI('open_file_dialog', false);
    if (res.code === 200 && res.data.file_path) {
      const result = await baseAPI('get_local_file_base64', res.data.file_path);
      if (result.code === 200) {
        // 清除当前画布状态
        clearMask();
        history.value = [];
        historyIndex.value = -1;
        
        // 加载新图片
        const img = new Image();
        img.onload = () => {
          originalImage.value = img;
          initCanvas(img);
        };
        img.src = result.data.base64_image;
      }
    }
  } catch (error) {
    message.error('Failed to load new image');
  } finally {
    loading.value = false;
  }
};

// Add keyboard event handler
const handleKeyboard = (event) => {
  // Process Image - Enter key
  if (event.key === 'Enter') {
    processImage();
  }
  
  // Download - Ctrl/Cmd + S
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault(); // Prevent browser's save dialog
    downloadImage();
  }
  
  // Undo - Ctrl/Cmd + Z
  if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key === 'z') {
    event.preventDefault();
    undo();
  }
  
  // Redo - Ctrl/Cmd + Shift + Z 或 Ctrl/Cmd + Y
  if ((event.ctrlKey || event.metaKey) && 
      ((event.shiftKey && event.key === 'z') || event.key === 'y')) {
    event.preventDefault();
    redo();
  }
};

// Add event listeners on mount and clean up on unmount
onMounted(() => {
  initImage();
  window.addEventListener('keydown', handleKeyboard);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyboard);
});
</script>

<style scoped>
.canvas-wrapper {
  padding-top: 1rem;
}

.canvas-container {
  position: relative;
  display: inline-block;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.base-canvas {
  display: block;
  border: 1px solid #ccc;
}

.mask-canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.eraser-cursor {
  position: absolute;
  border: 2px solid #fff;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.toolbar-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.toolbar {
  background-color: rgba(0, 0, 0, 0.5);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}

.toolbar__button {
  background-color: transparent;
  border: 0;
  color: #fff;
  cursor: pointer;
  width: 2rem;
  height: 2rem;
  border-radius: 0.25rem;
}

.toolbar__button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.toolbar__button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loader {
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
