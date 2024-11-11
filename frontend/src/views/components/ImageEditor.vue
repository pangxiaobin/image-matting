<template>
  <div class="image-editor" @mousemove="updateCursor" @wheel="handleZoom">
    <div class="canvas-container m-14" 
         :class="[{ 'move': mode === 'move', 'erase': mode === 'erase', 'restore': mode === 'restore' }, backgroundClass]"
         :style="{ backgroundColor: backgroundColor }"
         @mouseleave="handleMouseLeave"
         @mousedown="startInteraction"
         @mouseup="stopInteraction"
         @mousemove="handleInteraction">
      <canvas ref="displayCanvas" />
      <canvas ref="fullResCanvas" style="display: none;" />
      <canvas ref="originCanvas" style="display: none;" />
      <div v-if="showCursor && (mode === 'erase' || mode === 'restore')" class="eraser-cursor" :style="cursorStyle"></div>
    </div>
    <div class="toolbar flex mt-4 flex-wrap justify-center">
      <button class="toolbar__button" @click="undo" title="Undo">
        <i class="fa-solid fa-rotate-left"></i>
      </button>
      <button class="toolbar__button" @click="redo" title="Redo">
        <i class="fa-solid fa-rotate-right"></i>
      </button>
      <button class="toolbar__button" @click="zoomIn" title="Zoom In">
        <i class="fa-solid fa-magnifying-glass-plus"></i>
      </button>
      <span class="toolbar__text">
        {{ Math.round(zoom * 100) }}%
      </span>
      <button class="toolbar__button" @click="zoomOut" title="Zoom Out">
        <i class="fa-solid fa-magnifying-glass-minus"></i>
      </button>
      <button class="toolbar__button" @click="resetZoom" title="Reset Zoom">
        <i class="fa-solid fa-expand"></i>
      </button>
      <button class="toolbar__button" @click="setMode('move')" :class="{ 'active': mode === 'move' }" title="Move">
        <i class="fa-solid fa-arrows"></i>
      </button>
      <button class="toolbar__button" @click="setMode('erase')" :class="{ 'active': mode === 'erase' }" title="Erase">
        <i class="fa-solid fa-eraser"></i>
      </button>
      <button class="toolbar__button" @click="setMode('restore')" :class="{ 'active': mode === 'restore' }" title="Restore">
        <i class="fa-solid fa-window-restore"></i>
      </button>
      <button class="toolbar__button" @click="exportImage" title="Done">
        <i class="fa-solid fa-circle-check"></i>
      </button>
      <span class="toolbar__text">
        <input type="range" min="1" max="200" v-model="eraserSize" class="mr-2" /> {{ eraserSize }}
      </span>
      <button class="toolbar__button relative" @click="toggleBackgroundPicker" title="Change Background">
        <i class="fa-solid fa-palette"></i>
        <div v-if="showBackgroundPicker"
            class="absolute right-0 bottom-full mb-2 bg-white p-2 shadow-lg rounded-lg border z-20 w-24">
            <div class="grid grid-cols-2 gap-1">
              <div v-for="color in colors" :key="color" 
                :style="{ backgroundColor: color === 'checkerboard' ? 'transparent' : color }"
                @click="handleColorChange(color)" 
                class="w-10 h-10 cursor-pointer border"
                :class="{ 
                  'border-black': selectedColor === color, 
                  'checkerboard-background': color === 'checkerboard'
                }">
              </div>
            </div>
          </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue';

const displayCanvas = ref(null);
const fullResCanvas = ref(null);
const displayCtx = ref(null);
const fullResCtx = ref(null);
const isErasing = ref(false);
const baseImage = ref(null);
const eraserSize = ref(30);

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
  originBase64: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['exportImage']);

const scale = ref(1);

const zoom = ref(1);
const offsetX = ref(0);
const offsetY = ref(0);
const isDragging = ref(false);
const dragStartX = ref(0);
const dragStartY = ref(0);
const mode = ref('move'); // 默认模式为 'move'

const cursorStyle = computed(() => ({
  top: `${cursorY.value - eraserSize.value * zoom.value / 2}px`,
  left: `${cursorX.value - eraserSize.value * zoom.value / 2}px`,
  width: `${eraserSize.value * zoom.value}px`,
  height: `${eraserSize.value * zoom.value}px`,
  borderRadius: '50%',
  border: '1px solid red',
  position: 'absolute',
  pointerEvents: 'none',
  display: (mode.value === 'erase' || mode.value === 'restore') && showCursor.value ? 'block' : 'none',
}));

const backgroundColor = ref('');
const backgroundClass = ref('checkerboard-background');
const showBackgroundPicker = ref(false);
const colors = ['checkerboard', '#FFFFFF', '#000000', '#FF0000', '#00FF00', '#FFFF00', '#0000FF', '#FF00FF', '#00FFFF', '#C0C0C0' ];

const originCanvas = ref(null);
const originCtx = ref(null);
const originImage = ref(null);

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

function handleMouseLeave() {
  stopErasing();
  hideCursor();
}

function adjustCanvasSize(img) {
  const canvasWidth = 700;
  const canvasHeight = 500;

  const { width, height } = img;

  // Set full resolution canvas size
  fullResCanvas.value.width = width;
  fullResCanvas.value.height = height;

  // Set display canvas size
  displayCanvas.value.width = canvasWidth;
  displayCanvas.value.height = canvasHeight;

  // Calculate scale for display canvas
  const widthRatio = canvasWidth / width;
  const heightRatio = canvasHeight / height;
  scale.value = Math.min(widthRatio, heightRatio);

  // Calculate initial zoom
  const maxDimension = Math.max(width, height);
  const targetMaxDimension = Math.min(canvasWidth, canvasHeight)*1.2; // 90% of the smaller canvas dimension
  zoom.value = Math.min(1, targetMaxDimension / maxDimension);

  // Calculate offset to center the image
  offsetX.value = (canvasWidth - width * zoom.value) / 2;
  offsetY.value = (canvasHeight - height * zoom.value) / 2;

  // Set origin canvas size
  if (originCanvas.value) {
    originCanvas.value.width = width;
    originCanvas.value.height = height;
  }
}

function drawImage() {
  if (displayCanvas.value && fullResCanvas.value && baseImage.value) {
    // 绘制到全分辨率画布
    fullResCtx.value.clearRect(0, 0, fullResCanvas.value.width, fullResCanvas.value.height);
    fullResCtx.value.drawImage(baseImage.value, 0, 0, fullResCanvas.value.width, fullResCanvas.value.height);

    // 更新显示画布
    updateCanvas();
  }
}

function stopErasing() {
  if (isErasing.value) {
    isErasing.value = false;
    saveState();
  }
}

function updateCursor(e) {
  const rect = displayCanvas.value.getBoundingClientRect();
  cursorX.value = e.clientX - rect.left;
  cursorY.value = e.clientY - rect.top;

  if (cursorX.value < 0 || cursorY.value < 0 || cursorX.value > displayCanvas.value.width || cursorY.value > displayCanvas.value.height) {
    showCursor.value = false;
  } else {
    showCursor.value = true;
  }
}

function hideCursor() {
  showCursor.value = false;
}

function saveState() {
  const canvasData = fullResCanvas.value.toDataURL();
  if (history.currentIndex < history.states.length - 1) {
    history.states.splice(history.currentIndex + 1);
  }
  history.states.push(canvasData);
  history.currentIndex++;

  if (history.states.length > 20) {
    history.states.shift();
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
    fullResCtx.value.clearRect(0, 0, fullResCanvas.value.width, fullResCanvas.value.height);
    fullResCtx.value.drawImage(img, 0, 0, fullResCanvas.value.width, fullResCanvas.value.height);
    updateCanvas();
  };
}

function exportImage() {
  const base64Data = fullResCanvas.value.toDataURL('image/png');
  emit('export-image', base64Data);
}

function handleZoom(e) {
  e.preventDefault();
  const factor = e.deltaY > 0 ? 0.9 : 1.1;
  const rect = displayCanvas.value.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;
  
  changeZoomWithFocus(factor, mouseX, mouseY);
}

function resetZoom() {
  zoom.value = 1;
  offsetX.value = 0;
  offsetY.value = 0;
  updateCanvas();
}

function setMode(newMode) {
  mode.value = newMode;
}

function startInteraction(e) {
  if (mode.value === 'move') {
    isDragging.value = true;
    dragStartX.value = e.clientX - offsetX.value;
    dragStartY.value = e.clientY - offsetY.value;
  } else if (mode.value === 'erase' || mode.value === 'restore') {
    isErasing.value = true;
    handleBrush(e);
  }
}

function stopInteraction() {
  isDragging.value = false;
  if (isErasing.value) {
    stopErasing();
  }
}

function handleInteraction(e) {
  if (mode.value === 'move' && isDragging.value) {
    offsetX.value = e.clientX - dragStartX.value;
    offsetY.value = e.clientY - dragStartY.value;
    updateCanvas();
  } else if ((mode.value === 'erase' || mode.value === 'restore') && isErasing.value) {
    handleBrush(e);
  }
}

function updateCanvas() {
  if (displayCanvas.value && fullResCanvas.value) {
    const ctx = displayCanvas.value.getContext('2d');
    ctx.clearRect(0, 0, displayCanvas.value.width, displayCanvas.value.height);
    ctx.save();
    ctx.translate(offsetX.value, offsetY.value);
    ctx.scale(zoom.value, zoom.value);
    ctx.drawImage(fullResCanvas.value, 0, 0);
    ctx.restore();
  }
}

onMounted(() => {
  displayCtx.value = displayCanvas.value.getContext('2d');
  fullResCtx.value = fullResCanvas.value.getContext('2d');
  originCtx.value = originCanvas.value.getContext('2d');
  if (props.initialBase64) {
    loadImage(props.initialBase64);
  }
  if (props.originBase64) {
    loadOriginImage(props.originBase64);
  }
});

function zoomIn() {
  changeZoom(1.1);
}

function zoomOut() {
  changeZoom(0.9);
}

function changeZoom(factor) {
  const oldZoom = zoom.value;
  zoom.value = Math.max(0.1, Math.min(5, zoom.value * factor));

  // 调整偏移以保持画布中心不变
  const canvasRect = displayCanvas.value.getBoundingClientRect();
  const centerX = canvasRect.width / 2;
  const centerY = canvasRect.height / 2;
  
  offsetX.value = centerX - (centerX - offsetX.value) * (zoom.value / oldZoom);
  offsetY.value = centerY - (centerY - offsetY.value) * (zoom.value / oldZoom);

  updateCanvas();
}

function changeZoomWithFocus(factor, focusX, focusY) {
  const oldZoom = zoom.value;
  zoom.value = Math.max(0.1, Math.min(5, zoom.value * factor));

  // 调整偏移以保持焦点位置不变
  offsetX.value = focusX - (focusX - offsetX.value) * (zoom.value / oldZoom);
  offsetY.value = focusY - (focusY - offsetY.value) * (zoom.value / oldZoom);

  updateCanvas();
}

function toggleBackgroundPicker() {
  showBackgroundPicker.value = !showBackgroundPicker.value;
}

function handleColorChange(color) {
  setBackground(color);
  showBackgroundPicker.value = false;
}

function setBackground(color) {
  if (color === 'checkerboard') {
    backgroundColor.value = '';
    backgroundClass.value = 'checkerboard-background';
  } else {
    backgroundColor.value = color;
    backgroundClass.value = '';
  }
}

function loadOriginImage(base64) {
  const img = new Image();
  img.src = base64;
  img.onload = () => {
    originImage.value = img;
    if (originCanvas.value) {
      originCanvas.value.width = img.width;
      originCanvas.value.height = img.height;
      originCtx.value.drawImage(img, 0, 0);
    }
  };
}

function handleBrush(e) {
  if (isErasing.value && displayCtx.value && fullResCtx.value) {
    const rect = displayCanvas.value.getBoundingClientRect();
    const x = (e.clientX - rect.left - offsetX.value) / zoom.value;
    const y = (e.clientY - rect.top - offsetY.value) / zoom.value;

    showCursor.value = true;

    if (mode.value === 'erase') {
      erase(x, y);
    } else if (mode.value === 'restore') {
      restore(x, y);
    }

    updateCanvas();
  }
}

function erase(x, y) {
  applyBrush(x, y, 'destination-out');
}

function restore(x, y) {
  const ctx = fullResCtx.value;
  const canvas = fullResCanvas.value;
  const radius = eraserSize.value / 2;

  ctx.save();
  
  // 创建一个裁剪区域，限制绘制范围在画布内
  ctx.beginPath();
  ctx.rect(0, 0, canvas.width, canvas.height);
  ctx.clip();

  // 绘制原始图像的一部分
  ctx.globalCompositeOperation = 'source-over';
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2, false);
  ctx.clip();
  ctx.drawImage(originCanvas.value, 0, 0);

  ctx.restore();
}

function applyBrush(x, y, operation) {
  const ctx = fullResCtx.value;
  const canvas = fullResCanvas.value;
  const radius = eraserSize.value / 2;

  ctx.save();
  ctx.globalCompositeOperation = operation;

  // 创建一个裁剪区域，限制绘制范围在画布内
  ctx.beginPath();
  ctx.rect(0, 0, canvas.width, canvas.height);
  ctx.clip();

  // 绘制圆形笔刷
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2, false);
  ctx.fill();

  ctx.restore();
}
</script>

<style scoped>
.canvas-container {
  position: relative;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  overflow: hidden;
}

.checkerboard-background {
  background-image:
    linear-gradient(45deg, #ccc 25%, transparent 25%),
    linear-gradient(-45deg, #ccc 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #ccc 75%),
    linear-gradient(-45deg, transparent 75%, #ccc 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

.canvas-container.move {
  cursor: move;
}

.canvas-container.erase,
.canvas-container.restore {
  cursor: none;
}

canvas {
  display: block;
}

.eraser-cursor {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.1);
  pointer-events: none;
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

.toolbar__button.active {
  background-color: #0074d9;
}

.background-picker {
  position: absolute;
  bottom: 0;
  transform: translateX(-50%);
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 5px;
  display: flex;
  gap: 5px;
}

.color-option {
  width: 20px;
  height: 20px;
  border: none;
  cursor: pointer;
}

.color-option.checkerboard {
  background-image:
    linear-gradient(45deg, #ccc 25%, transparent 25%),
    linear-gradient(-45deg, #ccc 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #ccc 75%),
    linear-gradient(-45deg, transparent 75%, #ccc 75%);
  background-size: 10px 10px;
  background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
}
</style>