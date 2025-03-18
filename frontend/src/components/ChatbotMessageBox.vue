<!-- The area to write your message for the chatbot -->

<template>
    <div class="messageBox">
      <textarea
        ref="messageTextarea"
        id="messageInput"
        :placeholder="placeholder"
        v-model="message"
        rows="1"
        @input="autoResize"
        :disabled="isLoading"
      ></textarea>
      <button
        id="sendButton"
        @click="sendMessage"
        :disabled="isLoading"
      >
        <div v-if="isLoading">
          <div class="spinner"></div>
        </div>
        <div v-else class="svg-container" @mouseover="showTooltip = true" @mouseleave="showTooltip = false">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
              <path
                fill="none"
                d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
              />
              <path
                stroke-linejoin="round"
                stroke-linecap="round"
                stroke-width="33.67"
                stroke="#6c6c6c"
                d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
              />
            </svg>
            <div v-if="showTooltip" class="tooltip">Send message</div>
        </div>
      </button>
    </div>
  </template>
  
  <script>
    export default {
      name: 'EnhancedMessageBox',
      emits: ['messageSent'],
      props: {
        placeholder: {
          type: String,
          required: true,
          default: "Describe your animal characters with their behaviors...",
        }
      },
      data() {
        return {
          showTooltip: false,
          message: '',
          isLoading: false,
        };
      },
      mounted() {
        this.autoResize();
      },
      methods: {
        sendMessage() {
          // What happens when the send button is clicked
          if (!this.isLoading && (this.message.trim() !== '')) {
            this.isLoading = true;
            this.$emit('messageSent', this.message);
            this.autoResize();
          }
          this.$nextTick(() => {
            this.autoResize();
          });
        },
        autoResize() {
          // To resize the height of the box and scroll
          const textarea = this.$refs.messageTextarea;
          textarea.style.height = 'auto';
          textarea.style.height = `${textarea.scrollHeight}px`;
        },
      },
    };
  </script>
  
  <style scoped>
    .messageBox {
      width: 50vw;
      display: flex;
      align-items: flex-start;
      background-color: #2d2d2d;
      padding: 10px 15px;
      border-radius: 10px;
      border: 1px solid rgb(63, 63, 63);
      transition: border 0.3s;
    }
  
    .messageBox:focus-within {
      border: 1px solid rgb(110, 110, 110);
    }
  
    #messageInput {
      flex: 1;
      background-color: transparent;
      outline: none;
      border: none;
      color: white;
      font-size: 1.3em;
      line-height: 1.3em;
      padding: 5px 0 5px 5px;
      resize: none;
      min-height: 5vh;
      max-height: 25vh;
      overflow-y: auto;
      box-sizing: border-box;
      text-align: justify;
    }
  
    #messageInput::-webkit-scrollbar {
        width: 6px;
      }
      #messageInput::-webkit-scrollbar-track {
        background: #3c3c3c;
        border-radius: 3px;
      }
      #messageInput::-webkit-scrollbar-thumb {
        background: #666;
        border-radius: 3px;
      }
      #messageInput::-webkit-scrollbar-thumb:hover {
        background: #888;
      }
  
    #messageInput:disabled {
      background-color: #3c3c3c;
      color: #999;
    }
  
    #sendButton {
      align-self: flex-end;
      background-color: transparent;
      outline: none;
      border: none;
      display: flex;
      cursor: pointer;
      margin-right: -5px;
      margin-bottom: 0.2em;
      transition: all 0.3s;
    }
  
    #sendButton:disabled {
      cursor: not-allowed;
      opacity: 0.5;
    }
  
    #sendButton svg {
      height: 18px;
      transition: all 0.3s;
    }
  
    #sendButton svg path {
      fill: #3c3c3c;
      stroke: white;
      transition: all 0.3s;
    }
  
    #sendButton:hover svg path {
      fill: #cbcbcb;
    }
  
    .spinner {
      border: 3px solid #f3f3f3;
      border-top: 3px solid #6c6c6c;
      border-radius: 50%;
      width: 18px;
      height: 18px;
      animation: spin 1s linear infinite;
    }
  
    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  
    .svg-container {
      position: relative;
      display: inline-block;
    }
  
    .tooltip {
      position: absolute;
      top: -40px;
      transform: translateX(-50%);
      background-color: #4f4f4f;
      color: #fff;
      padding: 5px 10px;
      border-radius: 5px;
      font-size: 14px;
      white-space: nowrap;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
      pointer-events: none;
      z-index: 1000;
      opacity: 0;
      transition: opacity 0.2s ease-in-out;
    }
  
    .svg-container:hover .tooltip {
      opacity: 1;
    }
  </style>