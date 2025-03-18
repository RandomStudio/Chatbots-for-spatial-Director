<template>
    <button class="btn-green" @click="handleClick">
      {{ text }}
    </button>
  </template>
  
  <script>
  export default {
    emits: ["click"],
    props: {
      text: {
        type: String,
        required: true,
        default: 'test'
      },
    },
    methods: {
      handleClick() {
        this.$emit("click");
      },
    },
  };
  </script>
  
  <style scoped>
  .btn-green {
    background-color: #28a745;
    color: white;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .btn-green:hover {
    background-color: #218838;
  }
  
  .btn-green:active {
    background-color: #1e7e34;
    transform: scale(0.98);
  }

  .btn-green:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  </style>
  