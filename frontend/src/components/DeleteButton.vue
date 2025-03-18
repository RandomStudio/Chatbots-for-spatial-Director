<template>
    <button class="clearButton" @click="Restart">Start a new chat</button>
</template>

<script>
    export default {
        emits: [
            "restart"
        ],
        methods: {
            Restart() {
                this.$emit("restart");
            }
        }
    }
</script>

<style scoped>
    .clearButton {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.75em;
    box-shadow: 0 4px 8px rgba(255, 65, 108, 0.3);
    transition: all 0.3s ease-in-out;
    position: relative;
    overflow: hidden;
  }

  .clearButton:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255, 75, 43, 0.4);
  }

  .clearButton:active {
    transform: scale(0.95);
    box-shadow: 0 2px 6px rgba(255, 75, 43, 0.5);
  }

  .clearButton:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>