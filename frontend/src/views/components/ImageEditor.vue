<template>
  <div class="image-editor" @mousemove="updateCursor">
    <div class="canvas-container m-14" @mouseleave="handleMouseLeave">
      <canvas ref="canvas" @mousedown="startErasing" @mouseup="stopErasing" @mousemove="throttledErase" />
      <!-- 自定义光标显示 -->
      <div v-if="showCursor" class="eraser-cursor" :style="cursorStyle"></div>
    </div>
    <div class="toolbar flex mt-4 flex-wrap justify-center">

      <button class="toolbar__button" @click="undo" title="Undo">
        <i class="fa-solid fa-rotate-left"></i>
      </button>
      <button class="toolbar__button" @click="redo" title="Redo">
        <i class="fa-solid fa-rotate-right"></i>
      </button>
      <button class="toolbar__button" @click="exportImage" title="Done">
        <i class="fa-solid fa-circle-check"></i>
      </button>
      <span class="toolbar__text">
        <input type="range" min="5" max="100" v-model="eraserSize" class="mr-2" /> {{ eraserSize }}
      </span>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';

const throttle = (func, limit) => {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

const canvas = ref(null);
const ctx = ref(null);
const isErasing = ref(false);
const baseImage = ref(null);
const eraserSize = ref(10);

const showCursor = ref(false);
const cursorX = ref(0);
const cursorY = ref(0);

const history = reactive({
  states: [],
  currentIndex: -1,
});

const props = defineProps({
  initialBase64: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['exportImage']);


watch(() => props.initialBase64, (newVal) => {
  if (newVal) {
    loadImage(newVal);
  }
}, { immediate: true });

function loadImage(base64) {
  const img = new Image();
  img.src = base64;
  img.onload = () => {
    baseImage.value = img;
    adjustCanvasSize(img);
    drawImage();
    saveState();
  };
}

// 鼠标移出时停止擦除
function handleMouseLeave() {
  stopErasing();  // 停止擦除
  hideCursor();  // 隐藏光标
}

function adjustCanvasSize(img) {
  const maxCanvasWidth = 800;
  const maxCanvasHeight = 600;

  const { width, height } = img;

  let canvasWidth = width;
  let canvasHeight = height;

  if (width > maxCanvasWidth || height > maxCanvasHeight) {
    const widthRatio = maxCanvasWidth / width;
    const heightRatio = maxCanvasHeight / height;
    const scale = Math.min(widthRatio, heightRatio);

    canvasWidth = width * scale;
    canvasHeight = height * scale;
  }

  canvas.value.width = canvasWidth;
  canvas.value.height = canvasHeight;
}

function drawImage() {
  if (canvas.value && baseImage.value) {
    ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
    ctx.value.drawImage(baseImage.value, 0, 0, canvas.value.width, canvas.value.height);
  }
}

function startErasing(e) {
  isErasing.value = true;
  erase(e);
}

function erase(e) {
  if (isErasing.value && ctx.value) {
    const rect = canvas.value.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;


    if (cursorX.value < 0 || cursorY.value < 0 || cursorX.value > canvas.value.width || cursorY.value > canvas.value.height) {
      showCursor.value = false;
    } else {
      showCursor.value = true;
    }

    // 设置合成操作为擦除
    ctx.value.globalCompositeOperation = 'destination-out';

    // 使用圆形路径擦除
    ctx.value.beginPath();
    ctx.value.arc(x, y, eraserSize.value / 2, 0, Math.PI * 2, false);
    ctx.value.fill();

    // 还原为默认的绘图操作
    ctx.value.globalCompositeOperation = 'source-over';
  }
}

const throttledErase = throttle(erase, 8);

function stopErasing() {
  if (isErasing.value) {
    isErasing.value = false;
    saveState();
  }
}


function updateCursor(e) {
  const rect = canvas.value.getBoundingClientRect();
  cursorX.value = e.clientX - rect.left;
  cursorY.value = e.clientY - rect.top;

  if (cursorX.value < 0 || cursorY.value < 0 || cursorX.value > canvas.value.width || cursorY.value > canvas.value.height) {
    showCursor.value = false;
  } else {
    showCursor.value = true;
  }
}

function hideCursor() {
  showCursor.value = false;
}

function saveState() {
  const canvasData = canvas.value.toDataURL();
  if (history.currentIndex < history.states.length - 1) {
    history.states.splice(history.currentIndex + 1);
  }
  history.states.push(canvasData);
  history.currentIndex++;

  if (history.states.length > 20) {
    history.states.shift(); // 限制历史记录的长度为 20
    history.currentIndex--;
  }
}

function undo() {
  if (history.currentIndex > 0) {
    history.currentIndex--;
    restoreCanvas(history.states[history.currentIndex]);
  }
}

function redo() {
  if (history.currentIndex < history.states.length - 1) {
    history.currentIndex++;
    restoreCanvas(history.states[history.currentIndex]);
  }
}



function restoreCanvas(base64) {
  const img = new Image();
  img.src = base64;
  img.onload = () => {
    ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
    ctx.value.drawImage(img, 0, 0, canvas.value.width, canvas.value.height);
  };
}

function clearCanvas() {
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
  saveState();
}

function exportImage() {
  const base64Data = canvas.value.toDataURL('image/png');
  emit('export-image', base64Data);
}

onMounted(() => {
  ctx.value = canvas.value.getContext('2d');
  if (props.initialBase64) {
    loadImage(props.initialBase64);
  }
});

const cursorStyle = computed(() => ({
  top: `${cursorY.value - eraserSize.value / 2}px`,
  left: `${cursorX.value - eraserSize.value / 2}px`,
  width: `${eraserSize.value}px`,
  height: `${eraserSize.value}px`,
  borderRadius: '50%',
  border: '1px solid red',
  position: 'absolute',
  pointerEvents: 'none',
}));
</script>

<style scoped>
.canvas-container {
  position: relative;
  border: 1px solid #ccc;
  margin-bottom: 10px;
}

canvas {
  display: block;
}

.eraser-cursor {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.1);
}



.toolbar {
    background-color: rgba(0, 0, 0, 0.5);
    height: 2rem;
    width: auto;
    color: #fff;
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    align-items: center;
}

.toolbar__button {
    background-color: transparent;
    border: 0;
    color: #fff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    width: 2rem;
    height: 2rem;
    line-height: 1;
}

.toolbar__text {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    color: #fff;
}

.toolbar__button:hover {
    background-color: #0074d9;
}
</style>
