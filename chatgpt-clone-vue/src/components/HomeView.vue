<template>
  <section class="side-bar">
    <button @click="clearInput()">New Chat</button>
    <div class="history" v-if="history.length > 0">
      <div
        v-for="(message, index) in history"
        :key="index"
        class="history-item"
      >
        <input
          type="text"
          v-model="message.Content"
          v-if="isEditing && message.Id === editingId"
          @keyup.esc="cancelEditing"
          @keyup.enter="saveEditedMessage"
        />

        <template v-else>
          <p @click="getInputValue(message.Content)">
            {{ message.Content.substring(0, 18) + "..." }}
          </p>
          <div class="icons" v-show="!confirmDelete">
            <i class="fas fa-pencil-alt" @click="showEditing(message.Id)"></i>
            <i class="fas fa-trash" @click="showConfirmDelete"></i>
          </div>
          <div class="icons" v-show="confirmDelete">
            <i class="fas fa-check" @click="confirmDeleteItem(message.Id)"></i>
            <i class="fas fa-times" @click="cancelConfirmDelete"></i>
          </div>
        </template>
      </div>
    </div>

    <nav>
      <p>Made in Typescript</p>
    </nav>
  </section>

  <section class="main">
    <h1>AbdiGPT</h1>
    <p id="output">{{ responseContent }}</p>
    <div class="bottom-section">
      <div class="input-container">
        <input v-model="inputValue" @keyup.enter="getMessage()" />
        <div id="submit" @click="getMessage()">&#x27A2;</div>
      </div>
    </div>
    <p class="info">
      Chat GTP 1 Version Our goal is to make AI systems more natural and safe
      interract with. Your feedback will help us improve.
    </p>
  </section>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { MyRequestInit } from "../interfaces/my-request-init";
import { HistoryItem } from "../interfaces/history-item";
import { HistoryResponse } from "../interfaces/history-response";

export default defineComponent({
  name: "HomeView",
  setup() {
    // ----- Data -----
    const API_KEY: string = process.env.VUE_APP_API_KEY;
    const API_URI: string = process.env.VUE_APP_API_URI;

    const responseContent = ref<string>("");
    const inputValue = ref<string>("");
    const history = ref<HistoryItem[]>([]);
    const confirmDelete = ref<boolean>(false);
    const isEditing = ref<boolean>(false);
    const editingId = ref<number>(0);

    // ----- Functions -----
    const fetchHistory = async (): Promise<HistoryItem[]> => {
      try {
        let response = await fetch(API_URI);
        if (!response.ok) {
          throw new Error("Error fetching history");
        }
        let data: HistoryResponse = await response.json();
        return data.history;
      } catch (err) {
        console.log(err);
        throw new Error("Error fetching history");
      }
    };

    const postHistory = async (content: string): Promise<void> => {
      const options: MyRequestInit = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Content: content,
        }),
      };
      try {
        const response = await fetch(API_URI + "/add", options);

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const items = await fetchHistory();
        history.value = items.map((item: HistoryItem) => item);
      } catch (err) {
        console.error(err);
        throw new Error("Error posting message");
      }
    };

    const deleteHistory = async (id: number): Promise<void> => {
      const response = await fetch(API_URI + "/delete/" + id, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
    };

    const putHistory = async (id: number, content: string): Promise<void> => {
      const options: MyRequestInit = {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Content: content,
        }),
      };
      try {
        const response = await fetch(API_URI + "/update/" + id, options);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const items = await fetchHistory();
        history.value = items.map((item: HistoryItem) => item);
      } catch (err) {
        console.log(err);
        throw new Error("Error updating message");
      }
    };

    const showConfirmDelete = (): void => {
      confirmDelete.value = true;
    };

    const cancelConfirmDelete = (): void => {
      confirmDelete.value = false;
    };

    const confirmDeleteItem = async (id: number): Promise<void> => {
      try {
        await deleteHistory(id);
        const items = await fetchHistory();
        history.value = items.map((item: HistoryItem) => item);
        cancelConfirmDelete();
      } catch (err) {
        console.log(err);
        throw new Error("Error delete message");
      } finally {
        cancelConfirmDelete();
      }
    };

    const showEditing = (id: number): void => {
      isEditing.value = true;
      editingId.value = id;
    };

    const saveEditedMessage = (): void => {
      const editedMessageIndex = history.value.findIndex(
        (message) => message.Id === editingId.value
      );

      if (editedMessageIndex !== -1) {
        putHistory(
          history.value[editedMessageIndex].Id,
          history.value[editedMessageIndex].Content
        )
          .then(() => {
            inputValue.value = history.value[editedMessageIndex].Content;
            isEditing.value = false;
          })
          .catch((err) => {
            isEditing.value = false;
            console.log(err);
          });
      }
    };

    // Mounted
    onMounted(() => {
      fetchHistory().then((items: HistoryItem[]) => {
        history.value = items.map((item: HistoryItem) => item);
      });
    });

    return {
      API_KEY,
      API_URI,
      responseContent,
      inputValue,
      history,
      fetchHistory,
      postHistory,
      deleteHistory,
      putHistory,
      confirmDelete,
      showConfirmDelete,
      cancelConfirmDelete,
      confirmDeleteItem,
      isEditing,
      showEditing,
      editingId,
      saveEditedMessage,
    };
  },
  methods: {
    async getMessage(): Promise<void> {
      if (this.inputValue) {
        const options: MyRequestInit = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.API_KEY}`,
          },
          body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: this.inputValue }],
            max_tokens: 100,
          }),
        };

        try {
          const response = await fetch(
            "https://api.openai.com/v1/chat/completions",
            options
          );
          const data = await response.json();
          this.responseContent = data.choices[0].message.content;

          if (data.choices[0]?.message?.content && this.inputValue) {
            this.postHistory(this.inputValue);
          }
        } catch (err) {
          console.log(err);
          throw new Error("Error with openai API");
        }
      }
    },
    clearInput(): void {
      this.inputValue = "";
    },
    getInputValue(value: string): void {
      this.inputValue = value;
    },
    cancelEditing(): void {
      this.isEditing = false;
    },
  },
});
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap");

* {
  color: #fff;
  font-family: "Open Sans", sans-serif;
}

body {
  margin: 0;
  padding: 0;
  background-color: #343541;
  display: flex;
}

h1 {
  font-size: 33px;
  font-weight: 600;
  padding: 200px 0;
}

.side-bar {
  background-color: #202123;
  width: 244px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  justify-content: space-between;
  height: 100vh;
  width: 100%;
}

.bottom-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.info {
  color: rgba(255, 255, 255, 0.5);
  font-size: 11px;
  padding: 10px;
}

input {
  border: none;
  background-color: rgba(255, 255, 255, 0.05);
  width: 100%;
  font-size: 20px;
  padding: 12px 15px;
  border-radius: 5px;
  box-shadow: rgb(0, 0, 0, 0.05) 0 54px 55px,
    rgb(0, 0, 0, 0.05) 0 -12px 30px rgb(0, 0, 0, 0.05) 0 4px 6px rgb(
        0,
        0,
        0,
        0.05
      ) 0 12px 3px rgb(0, 0, 0, 0.09) 0 -3px 5px;
}

input:focus {
  outline: none;
}

.input-container {
  position: relative;
  width: 100%;
  max-width: 650px;
}

.input-container #submit {
  position: absolute;
  right: 0;
  bottom: 15px;
  cursor: pointer;
}

button {
  border: solid 0.5px rgba(255, 255, 255, 0.05);
  background-color: transparent;
  border-radius: 5px;
  padding: 10px;
  margin: 10px;
}

nav {
  border-top: solid 0.5px rgba(255, 255, 255, 0.05);
  padding: 10px;
  margin: 10px;
}

.history {
  padding: 10px;
  margin: 10px;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: auto;
}

.history p {
  cursor: pointer;
}

.history::-webkit-scrollbar {
  width: 10px;
  background-color: #fff;
}

.history::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: #999;
}

.history::-webkit-scrollbar-thumb:hover {
  background-color: #777;
}

.history::-webkit-scrollbar-track {
  background-color: #202123;
}

.history::-webkit-scrollbar-button {
  display: none;
}

.history::-webkit-scrollbar-corner {
  background-color: transparent;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icons {
  display: flex;
}

.icons i {
  margin-left: 10px;
  cursor: pointer;
}

.icons i:hover {
  color: red;
}
</style>
