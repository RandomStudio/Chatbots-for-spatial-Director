<template>
    <DeleteButton style="position: fixed; top: 2vh; left: 1vw; z-index: 10;" @restart="Restart" :disabled="loading"></DeleteButton>
    <GenericButton style="position: fixed; top: 2vh; right: 1vw; z-index: 10;" :text="'Using the latest script for interacion'" @click="goToInteraction" :disabled="loading"></GenericButton>
    <div class="wrapper">
        <div class="history" ref="history">
            <div v-for="(message, index) in history" :key="index" :class="message.role">
                <div v-show="message.role != 'system'" class="message-bubble" v-html="convertGPTText(message.content)">
                </div>
            </div>
            <div v-show="loading" style="align-self: flex-start; display: flex; padding: 10px;">
                <LoadingDots></LoadingDots>
            </div>
        </div>
        <div class="foot">
            <ChatbotMessageBox @message-sent="messageSent" ref="messagebox" :placeholder="'Describe your animal characters with their behaviors...'"></ChatbotMessageBox>
        </div>
    </div>
</template>

<script>
    import ChatbotMessageBox from './ChatbotMessageBox.vue';
    import LoadingDots from './LoadingDots.vue';
    import DeleteButton from './DeleteButton.vue';
    import GenericButton from './GenericButton.vue';
    import { marked } from "marked";

    export default {
        components: {
            ChatbotMessageBox,
            LoadingDots,
            DeleteButton,
            GenericButton
        },
        data() {
            return {
                history: [{"role":"system",
                "content":`I will pass you a text describing characters. I assigned to each character an animal based on their way to move around the scene.
        Those characters are animals that have specific personalities based on the analysis of their movements.
        I want you to write a short storyline involving those characters.
        Characters can interact with each other and will live a short adventure (about 5 minutes actions) with a beginning and an end.
        Include three different static props elements on the scene the characters can interact with (can be a tree, a house, a river...). Those elements are static and can't be moved at any moment of the play.
        You will also have to decide an environment for the scene among those dutch environment:
        - Amsterdam canal
        - A polder
        - Het Amsterdamse Bos (Suburb Forest)

        The characters can't speak, they just make animal sounds.
        ALWAYS AND ONLY return without other comments this script which should include:
        - The title of the play
        - The animals (don't name them)
        - The environment
        - The 3 props
        - The storyline
        
        Note that the final goal is to reward improvisation of the actors, therefore stay really open in your description with not much details.`}],
                loading:false,
                sessionId: null,
                threadId: null,
            }
        },
        mounted() {
            this.$nextTick(() => {
                const latest_script = localStorage.getItem("script");
                if (latest_script != null) this.history.push({"role":"assistant", "content": latest_script});
            });
        },
        methods: {
            async messageSent(message) {
                this.loading = true;
                this.history.push({"role":"user", "content":message});
                this.scrollToBottom();
                const formData = new URLSearchParams();
                formData.append("history", JSON.stringify(this.history));

                const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/chatCompletion`, {
                    method: "POST",
                    body: formData,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let done;
                let answer="";
                const index = this.history.length;
                while (!done) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    if (answer=="") {
                        this.history.push({"role":"assistant", "content":answer});
                    }
                    answer += decoder.decode(value)
                    this.history[index]["content"] = answer;
                }

                this.loading = false;
                this.$refs.messagebox.message = "";
                this.$nextTick(() => {this.$refs.messagebox.autoResize()});
                this.$refs.messagebox.isLoading = false;
            },
            convertGPTText(text) {
                return marked(text);
            },
            scrollToBottom() {
                this.$nextTick(() => {
                    const historyDiv = this.$refs.history;
                    if (historyDiv) {
                        historyDiv.scrollTop = historyDiv.scrollHeight;
                    }
                });
            },
            Restart() {
                if (this.history != []) {
                    this.history = [this.history[0]];
                }
            },
            goToInteraction() {
                if (this.history.filter(obj => obj.role == 'assistant').length == 0) {
                    alert("Try generating a script first");
                }
                else {
                    const script = this.history.filter(obj => obj.role == 'assistant').at(-1).content;
                    localStorage.setItem("script", script);
                    window.location.href = './interaction';
                }
            }
        }
    }
</script>

<style>
.wrapper {
    position: fixed;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Message container: ensure messages don't touch each other */
.history {
    flex-grow: 1;
    width: 50vw;
    margin-left: calc(25vw - 10px);
    margin-top: 1vh;
    margin-bottom: 2vh;
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: flex-start; /* Ensures messages align correctly */
    background-color: #2d2d2d;
    overflow-y: auto;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    padding: 15px;
    scroll-behavior: smooth;
}

/* Adds space between different roles */
.user + .assistant,
.assistant + .user {
    margin-top: 20px; /* Larger gap when the sender switches */
}

/* General spacing for messages */
.message-bubble {
    max-width: 60%;
    padding: 10px 15px;
    border-radius: 15px;
    font-size: 16px;
    word-wrap: break-word;
    text-align: left;
    background-color: #f1f1f1;
    color: black;
    display: inline-block;
    max-width: fit-content;
    margin-bottom: 8px; /* Keeps same role messages closer */
}

/* User message bubble (right-aligned) */
.user {
    align-self: flex-end; /* Aligns user messages to the right */
    display: flex;
    justify-content: flex-end;
    width: 100%;
}

/* Assistant message bubble (left-aligned) */
.assistant {
    align-self: flex-start;
    display: flex;
    justify-content: flex-start;
    width: 100%;
}

/* User message styling */
.user .message-bubble {
    background-color: #0078FF;
    color: white;
    border-radius: 15px 15px 0px 15px;
    text-align: left;
}

/* Assistant message styling */
.assistant .message-bubble {
    background-color: #F1F1F1;
    color: black;
    border-radius: 15px 15px 15px 0px;
    text-align: left;
    max-width: 60%;
}

/* Markdown elements spacing fixes */
.message-bubble p {
    margin: 0;
    padding: 0;
}

.message-bubble pre {
    background: #272822;
    color: #f8f8f2;
    padding: 8px;
    border-radius: 5px;
    overflow-x: auto;
    display: block;
}

.message-bubble code {
    background: none;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: monospace;
}

.message-bubble p {
    text-align: justify;
}

/* Ensure list items are aligned properly */
.message-bubble ul, .message-bubble ol {
    padding-left: 20px;
    margin: 5px 0;
}

/* Prevent markdown headers from adding unwanted space */
.message-bubble h1, 
.message-bubble h2, 
.message-bubble h3, 
.message-bubble h4, 
.message-bubble h5, 
.message-bubble h6 {
    margin: 5px 0;
    font-size: 1em;
    text-align: justify;
}

.foot {
    width: 100vw;
    position: relative;
    bottom: 1vh;
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: center;
}
</style>
