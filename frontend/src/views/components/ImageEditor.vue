<template>
  <div class="image-editor" @mousemove="updateCursor">
    <div class="canvas-container m-14" @mouseleave="handleMouseLeave">
      <canvas ref="displayCanvas" @mousedown="startErasing" @mouseup="stopErasing" @mousemove="throttledErase" />
      <!-- Hidden full-resolution canvas -->
      <canvas ref="fullResCanvas" style="display: none;" />
      <!-- Custom cursor display -->
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

const displayCanvas = ref(null);
const fullResCanvas = ref(null);
const displayCtx = ref(null);
const fullResCtx = ref(null);
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

const scale = ref(1);

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
  const maxCanvasWidth = 800;
  const maxCanvasHeight = 600;

  const { width, height } = img;

  // Set full resolution canvas size
  fullResCanvas.value.width = width;
  fullResCanvas.value.height = height;

  // Calculate scale for display canvas
  const widthRatio = maxCanvasWidth / width;
  const heightRatio = maxCanvasHeight / height;
  scale.value = Math.min(widthRatio, heightRatio, 1);

  // Set display canvas size
  displayCanvas.value.width = width * scale.value;
  displayCanvas.value.height = height * scale.value;
}

function drawImage() {
  if (displayCanvas.value && fullResCanvas.value && baseImage.value) {
    // Draw on full resolution canvas
    fullResCtx.value.clearRect(0, 0, fullResCanvas.value.width, fullResCanvas.value.height);
    fullResCtx.value.drawImage(baseImage.value, 0, 0, fullResCanvas.value.width, fullResCanvas.value.height);

    // Draw scaled version on display canvas
    displayCtx.value.clearRect(0, 0, displayCanvas.value.width, displayCanvas.value.height);
    displayCtx.value.drawImage(fullResCanvas.value, 0, 0, displayCanvas.value.width, displayCanvas.value.height);
  }
}

function startErasing(e) {
  isErasing.value = true;
  erase(e);
}

function erase(e) {
  if (isErasing.value && displayCtx.value && fullResCtx.value) {
    const rect = displayCanvas.value.getBoundingClientRect();
    const x = (e.clientX - rect.left) / scale.value;
    const y = (e.clientY - rect.top) / scale.value;

    if (x < 0 || y < 0 || x > fullResCanvas.value.width || y > fullResCanvas.value.height) {
      showCursor.value = false;
    } else {
      showCursor.value = true;
    }

    // Erase on full resolution canvas
    fullResCtx.value.globalCompositeOperation = 'destination-out';
    fullResCtx.value.beginPath();
    fullResCtx.value.arc(x, y, eraserSize.value / 2, 0, Math.PI * 2, false);
    fullResCtx.value.fill();
    fullResCtx.value.globalCompositeOperation = 'source-over';

    // Erase on display canvas
    displayCtx.value.globalCompositeOperation = 'destination-out';
    displayCtx.value.beginPath();
    displayCtx.value.arc(x * scale.value, y * scale.value, eraserSize.value * scale.value / 2, 0, Math.PI * 2, false);
    displayCtx.value.fill();
    displayCtx.value.globalCompositeOperation = 'source-over';
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
    
    displayCtx.value.clearRect(0, 0, displayCanvas.value.width, displayCanvas.value.height);
    displayCtx.value.drawImage(fullResCanvas.value, 0, 0, displayCanvas.value.width, displayCanvas.value.height);
  };
}

function clearCanvas() {
  fullResCtx.value.clearRect(0, 0, fullResCanvas.value.width, fullResCanvas.value.height);
  displayCtx.value.clearRect(0, 0, displayCanvas.value.width, displayCanvas.value.height);
  saveState();
}

function exportImage() {
  const base64Data = fullResCanvas.value.toDataURL('image/png');
  emit('export-image', base64Data);
}

onMounted(() => {
  displayCtx.value = displayCanvas.value.getContext('2d');
  fullResCtx.value = fullResCanvas.value.getContext('2d');
  if (props.initialBase64) {
    loadImage(props.initialBase64);
  }
});

const cursorStyle = computed(() => ({
  top: `${cursorY.value - eraserSize.value * scale.value / 2}px`,
  left: `${cursorX.value - eraserSize.value * scale.value / 2}px`,
  width: `${eraserSize.value * scale.value}px`,
  height: `${eraserSize.value * scale.value}px`,
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
