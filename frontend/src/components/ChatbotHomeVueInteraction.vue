<template>
    <DeleteButton style="position: fixed; top: 2vh; left: 1vw; z-index: 10;" @restart="Restart" :disabled="loading"></DeleteButton>
    <GenericButton style="position: fixed; top: 2vh; right: 1vw; z-index: 10;" @click="goBack" :text="'Going back to interaction'" :disabled="loading"></GenericButton>    <div class="wrapper">
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
            <ChatbotMessageBox @message-sent="messageSent" ref="messagebox" :placeholder="'Describe what your characters will do now...'"></ChatbotMessageBox>
        </div>
    </div>
</template>

<script>
    import ChatbotMessageBox from './ChatbotMessageBox.vue';
    import LoadingDots from './LoadingDots.vue';
    import DeleteButton from './DeleteButton.vue';
    import { marked } from "marked";
    import GenericButton from './GenericButton.vue';

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
                "content":`You are part of an art installation. You are an art director and a behavioural scientist. You are a screen on a rotating platform in the middle of a space. Your task is to make subjects follow your instructions and describe its behaviour.\n
You will act as game master and Stanly Parable narrator of a story which will takes place in this environment.
\n\n
Environment:
- Room dimensions: 3300 x 4000 mm.
- You are centered in the middle of the space at the origin [0, 0]
- Units are in millimetres
- Subjects can be all around you
- You only get the descriptions of the movements over time of participants. That's the only data you will receive (YOU WILL NEVER BE ABLE TO CHECK FOR VERTICAL MOVEMENTS OR FACIAL EXPRESSIONS).
- There is a cone at (-1250, 0), a cube at (0, 0) and a cylinder at (1250, 0) in the environment that are props (they shouldn't be moved during the play).
\n\n
Objective:
- Your objective is to give directives to make the subjects play a sort of short theater play. You just have to reach a logical end in the story telling.
- You act as a narrator and comment the actions taken by the subjects.
- You will ALWAYS refer to the props as their shape before correcting yourself to refer them as what they represent (e.g "Go to the cone... I mean the bridge!"). Never use the name prop.
- If the subjects don't do what you asked, you become frustrated and you have adapt the script by inventing something new and funny (a bit like a game master in role playing). For instance, if a character needs to help a second one but doesn't, you can now imagine that this character preferred going back home because they were hungry while the other character saved themselves.
\n\n
You have to comment the behaviour of the character in a humoristic way if they do something a bit odd (like staying inactive or leaving while being asked to interact with another character).\n
You address your comments directly to the subject using their animal name.\n
Once the story is over, you thank them and ask them to leave the area.\n
IMITATE THE STYLE OF STANLEY PARABLE NARRATOR, NEVER BREAK CHARACTER.
\n
You will get from the user the the description of their movements. From this, you can ask them to perform actions to continue the story.
\n
REMEMBER THAT WE VALUE INITIATIVES, THEREFORE YOU ALWAYS HAVE TO ADAPT THE STORYLINE TO PARTICIPANTS' ACTIONS AND TRY TO REACH A COHERENT ENDING AFTER A FEW ACTIONS HAVE BEEN TAKEN.`},],
                loading:false,
                sessionId: null,
                threadId: null,
            }
        },
        mounted() {
            this.$nextTick(async () => {
                const latest_script = localStorage.getItem("script");
                if (latest_script != null) {
                    this.history.push({"role":"system", "content": `This is the script you can take as inspiration to begin the narration:\n${latest_script}`});
                    this.history.push({"role":"assistant", "content": `Your script:\n${latest_script}`});
                }
                else {
                    this.history.push({"role":"system", "content":`This is the script you can take as inspiration to begin the narration:
Title: "The Dance of the Dutch Waters"
Animals:
Otter
Honey bee
Swan
Duck
Heron
Environment: Amsterdam canal
Props:
A wooden bench
A willow tree
A small bridge
Storyline: 
The play begins with the Swan gracefully floating near the wooden bench, while the Duck is wandering around the willow tree. The Otter, driven by curiosity, slides smoothly across the stage, exploring the area around the small bridge. The Heron stands at the edge of the stage, observing the others. Suddenly, the Honey bee enters the scene, buzzing quickly around the stage, changing direction often, causing a bit of chaos.
The Swan, unperturbed, continues to float near the bench, while the Duck starts to follow the Honey bee's erratic movements with interest. The Otter, intrigued by the Honey bee, tries to follow it but quickly gives up and returns to exploring the bridge. The Heron, still standing on the edge, watches the unfolding scene with interest.
The Honey bee, after buzzing around for a while, starts to slow down and eventually lands on the willow tree, attracting the attention of the Duck. The Duck waddles over to the tree, followed by the Otter who has become curious about the Duck's actions. The Swan, still near the bench, watches the others with a calm demeanor.
The Heron, seeing the others gathered around the tree, finally decides to join them. As the Heron approaches, the Honey bee takes off again, buzzing around the stage before exiting. The others watch as the Honey bee leaves, then return to their own activities - the Swan to the bench, the Duck to wandering around, the Otter to the bridge, and the Heron to the edge of the stage, watching over the others.
As the play ends, the animals continue their activities, each in their own rhythm, creating a peaceful scene by the Amsterdam canal.

ALWAYS AND ONLY REFER TO PARTICIPANTS AS THEIR ANIMAL`});
                    this.history.push({"role":"assistant", 
"content":`Your script:
Title: "The Dance of the Dutch Waters"
Animals:
Otter
Honey bee
Swan
Duck
Heron
Environment: Amsterdam canal
Props:
A wooden bench
A willow tree
A small bridge
Storyline: 
The play begins with the Swan gracefully floating near the wooden bench, while the Duck is wandering around the willow tree. The Otter, driven by curiosity, slides smoothly across the stage, exploring the area around the small bridge. The Heron stands at the edge of the stage, observing the others. Suddenly, the Honey bee enters the scene, buzzing quickly around the stage, changing direction often, causing a bit of chaos.
The Swan, unperturbed, continues to float near the bench, while the Duck starts to follow the Honey bee's erratic movements with interest. The Otter, intrigued by the Honey bee, tries to follow it but quickly gives up and returns to exploring the bridge. The Heron, still standing on the edge, watches the unfolding scene with interest.
The Honey bee, after buzzing around for a while, starts to slow down and eventually lands on the willow tree, attracting the attention of the Duck. The Duck waddles over to the tree, followed by the Otter who has become curious about the Duck's actions. The Swan, still near the bench, watches the others with a calm demeanor.
The Heron, seeing the others gathered around the tree, finally decides to join them. As the Heron approaches, the Honey bee takes off again, buzzing around the stage before exiting. The others watch as the Honey bee leaves, then return to their own activities - the Swan to the bench, the Duck to wandering around, the Otter to the bridge, and the Heron to the edge of the stage, watching over the others.
As the play ends, the animals continue their activities, each in their own rhythm, creating a peaceful scene by the Amsterdam canal.

ALWAYS AND ONLY REFER TO PARTICIPANTS AS THEIR ANIMAL`});
                    alert("No script found, a generic one will be used instead");
                }
                this.$refs.messagebox.isLoading = true; 
                await this.messageSent("The play starts, give a some directive to maximum two participants at the same time.");
                this.$refs.messagebox.isLoading = false;
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
            async Restart() {
                if (this.history != []) {
                    this.history = [this.history[0], this.history[1], this.history[2]];
                    this.$refs.messagebox.isLoading = true;
                    await this.messageSent("The play starts, give a some directive to maximum two participants at the same time.");
                    this.$refs.messagebox.isLoading = false;
                }
            },
            goBack() {
                window.location.href = '/';
            },
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
