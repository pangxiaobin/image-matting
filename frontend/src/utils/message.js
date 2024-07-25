// src/plugins/message.js
import { createApp, h } from 'vue';
import Message from '@/views/components/MessageComponent.vue';

const createMessage = (content, type = 'info', duration = 3000) => {
  const container = document.createElement('div');
  document.body.appendChild(container);

  const app = createApp({
    render() {
      return h(Message, { content, type, duration });
    },
  });

  app.mount(container);

  setTimeout(() => {
    app.unmount();
    document.body.removeChild(container);
  }, duration + 1000);
};

const message = {
  info(content, duration) {
    createMessage(content, 'info', duration);
  },
  success(content, duration) {
    createMessage(content, 'success', duration);
  },
  error(content, duration) {
    createMessage(content, 'error', duration);
  },
  warning(content, duration) {
    createMessage(content, 'warning', duration);
  },
};

export default message;