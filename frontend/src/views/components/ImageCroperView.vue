<template>
    <div class="editor h-full flex flex-col items-center">
        <div class="canvas relative w-full h-96" @dblclick="dblclick">
            <img :src="imageUrl" ref="image" @load="onImageLoad" class="object-contain w-full h-full" />
        </div>
        <div v-if="cropper" class="toolbar flex mt-4 flex-wrap justify-center" @click="handleClick">

            <button v-if="toolbarOptions.play" class="toolbar__button" data-action="play" title="Play (S)">
                <i class="fa-solid fa-circle-play"></i>
            </button>
            <!-- 删除 -->
            <button v-if="toolbarOptions.delete" class="toolbar__button" data-action="delete" title="Delete (Delete)">
                <span class="fa fa-trash"></span>
            </button>

            <button v-if="toolbarOptions.move" class="toolbar__button" data-action="move" title="Move (M)">
                <span class="fa fa-arrows"></span>
            </button>
            <button v-if="toolbarOptions.crop" class="toolbar__button" data-action="crop" title="Crop (C)">
                <span class="fa fa-crop"></span>
            </button>
            <button v-if="isCropping && toolbarOptions.cancel" class="toolbar__button" data-action="cancel"
                title="Cancel (CTRL + Z)">
                <span class="fa fa-times"></span>
            </button>
            <button v-if="isCropping && toolbarOptions.confirm" class="toolbar__button" data-action="confirm"
                title="Confirm (Enter)">
                <span class="fa fa-check"></span>
            </button>
            <button v-if="toolbarOptions.zoomIn" class="toolbar__button" data-action="zoom-in" title="Zoom In (I)">
                <span class="fa fa-search-plus"></span>
            </button>
            <button v-if="toolbarOptions.zoomOut" class="toolbar__button" data-action="zoom-out" title="Zoom Out (O)">
                <span class="fa fa-search-minus"></span>
            </button>
            <button v-if="toolbarOptions.rotateLeft" class="toolbar__button" data-action="rotate-left"
                title="Rotate Left (L)">
                <span class="fa fa-rotate-left"></span>
            </button>
            <button v-if="toolbarOptions.rotateRight" class="toolbar__button" data-action="rotate-right"
                title="Rotate Right (R)">
                <span class="fa fa-rotate-right"></span>
            </button>
            <button v-if="toolbarOptions.flipHorizontal" class="toolbar__button" data-action="flip-horizontal"
                title="Flip Horizontal (H)">
                <span class="fa fa-arrows-h"></span>
            </button>
            <button v-if="toolbarOptions.flipVertical" class="toolbar__button" data-action="flip-vertical"
                title="Flip Vertical (V)">
                <span class="fa fa-arrows-v"></span>
            </button>
            <!-- 展示图片类型 图片尺寸 -->

            <span class="toolbar__text">
                <span class="toolbar__text-item ml-2">{{ imageType }}</span>
                <span class="toolbar__text-item ml-2 mr-2">{{ imageWidth }}x{{ imageHeight }}</span>
            </span>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';

const props = defineProps({
    imageUrl: {
        type: String,
        required: true,
    },
    toolbarOptions: {
        type: Object,
        default: () => ({
            move: true,
            crop: true,
            cancel: true,
            confirm: true,
            zoomIn: true,
            zoomOut: true,
            rotateLeft: true,
            rotateRight: true,
            flipHorizontal: true,
            flipVertical: true,
            background: true,
            play: false,
            delete: false,
        }),
    },
    cropSize: String,
    play: Function,
    delete: Function,
});

const emit = defineEmits(['crop', 'cancel', 'confirm',]);

const image = ref(null);
const cropper = ref(null);
const isCropping = ref(false);
const croppedData = ref(null);
const canvasData = ref(null);
const cropBoxData = ref(null);

const imageWidth = ref(0);
const imageHeight = ref(0);
const imageType = ref('');
function onImageLoad() {
    if (!isCropping.value) {
        initializeCropper();

    }
    imageWidth.value = image.value.naturalWidth;
    imageHeight.value = image.value.naturalHeight;
    // 图片scr 判断是base64还是url，然后获取图片类型
    const src = image.value.src;
    if (src.startsWith('data:image/')) {
        imageType.value = src.split(';')[0].split('/')[1];
    } else {
        imageType.value = src.split('.').pop();
    }
}

function initializeCropper() {
    if (cropper.value) {
        cropper.value.destroy();
        cropper.value = null;
    }
    cropper.value = new Cropper(image.value, {
        autoCrop: false,
        dragMode: 'move',
        background: props.toolbarOptions.background,
        ready: () => {
            if (croppedData.value) {
                cropper.value
                    .crop()
                    .setData(croppedData.value)
                    .setCanvasData(canvasData.value)
                    .setCropBoxData(cropBoxData.value);

                croppedData.value = null;
                canvasData.value = null;
                cropBoxData.value = null;
            }
        },
        crop: ({ detail }) => {
            if (detail.width > 0 && detail.height > 0 && !isCropping.value) {
                isCropping.value = true;
            }
        },
    });
}

const setCropBox = () => {
    if (props.cropSize) {
        const [width, height] = props.cropSize.split('x').map(Number);
        cropper.value.setDragMode('crop');
        cropper.value.setAspectRatio(width / height);
        cropper.value.setCropBoxData({ width, height });
        cropper.value.crop();
    }
};

watch(() => props.cropSize, (newSize) => {
    console.log(newSize);
    if (newSize) {
        setCropBox();
    }
});

function handleClick({ target }) {
    const action = target.getAttribute('data-action') || target.parentElement.getAttribute('data-action');

    switch (action) {
        case 'move':
        case 'crop':
            cropper.value.setDragMode(action);
            cropper.value.setAspectRatio(null);
            break;
        case 'cancel':
            clear();
            emit('cancel');
            break;
        case 'confirm':
            confirm()
            break;
        case 'zoom-in':
            cropper.value.zoom(0.1);
            break;
        case 'zoom-out':
            cropper.value.zoom(-0.1);
            break;
        case 'rotate-left':
            cropper.value.rotate(-90);
            break;
        case 'rotate-right':
            cropper.value.rotate(90);
            break;
        case 'flip-horizontal':
            cropper.value.scaleX(-cropper.value.getData().scaleX || -1);
            break;
        case 'flip-vertical':
            cropper.value.scaleY(-cropper.value.getData().scaleY || -1);
            break;
        case 'play':
            play();
            break;
        case 'delete':
            delelte();
            break;
        default:
    }
}

async function play() {
    console.log('play');
    if (props.play) {
        const result = props.play();

        if (result instanceof Promise) {
            try {
                await result;
            } catch (error) {
                console.error("调用父组件方法时出错:", error);
            }
        } else {
            console.log("父组件的非 async 方法调用完成");
        }
    } else {
        console.log("父组件方法未传递");
    }
}

const delelte = () => {
    if (props.delete) {
        console.log('delete');
        props.delete();
    }
};

function clear() {
    if (isCropping.value) {
        cropper.value.clear();
        isCropping.value = false;
    }
}
const stop = () => {
    if (cropper.value) {
        cropper.value.destroy();
        cropper.value = null;
    }
    console.log('stop');
};

function crop() {
    if (isCropping.value) {
        croppedData.value = cropper.value.getData();
        canvasData.value = cropper.value.getCanvasData();
        cropBoxData.value = cropper.value.getCropBoxData();

        isCropping.value = false;
        stop();
    }

}

// 确认按钮点击事件
const confirm = () => {
    emit('confirm', cropper.value.getCroppedCanvas(imageType.value.toLowerCase === 'png' ? {} : {
            fillColor: '#fff',
          }).toDataURL("image/" + imageType.value));
    crop();
};

const dblclick = (e) => {
    if (e.target.className.indexOf('cropper-face') >= 0) {
        e.preventDefault();
        e.stopPropagation();
        crop();
    }
};

// js 键盘事件
const keydown = (e) => {
    if (!cropper.value) return;

    switch (e.key) {
        case 'z':
            if (e.ctrlKey) {
                e.preventDefault();
                clear();
            }
            break;
        case 'Enter':
            confirm()
            break;
        case 'Escape':
            clear();
            break;
        case 'ArrowLeft':
            e.preventDefault();
            cropper.value.move(-1, 0);
            break;
        case 'ArrowUp':
            e.preventDefault();
            cropper.value.move(0, -1);
            break;
        case 'ArrowRight':
            e.preventDefault();
            cropper.value.move(1, 0);
            break;
        case 'ArrowDown':
            e.preventDefault();
            cropper.value.move(0, 1);
            break;
        case 'c':
            cropper.value.setDragMode('crop');
            break;
        case 'm':
            cropper.value.setDragMode('move');
            break;
        case 'i':
            cropper.value.zoom(0.1);
            break;
        case 'o':
            cropper.value.zoom(-0.1);
            break;
        case 'l':
            cropper.value.rotate(-90);
            break;
        case 'r':
            cropper.value.rotate(90);
            break;
        case 'h':
            cropper.value.scaleX(-cropper.value.getData().scaleX || -1);
            break;
        case 'v':
            cropper.value.scaleY(-cropper.value.getData().scaleY || -1);
            break;
    }
};

onMounted(() => {
    window.addEventListener('keydown', keydown);
    if (!props.imageUrl) {
        clear();
    }
});

onBeforeUnmount(() => {
    window.removeEventListener('keydown', keydown);
    if (cropper.value) {
        cropper.value.destroy();
        cropper.value = null;
    }
});
</script>

<style scoped>
.editor {
    height: 100%;
}

.canvas {
    display: flex;
    align-items: center;
    justify-content: center;
}
.toolbar {
    background-color: rgba(0, 0, 0, 0.5);
    height: 2rem;
    width: auto;
    color: #fff;
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    align-items: center; /* 确保工具栏内的元素垂直居中 */
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
    line-height: 1; /* 确保文字垂直居中 */
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