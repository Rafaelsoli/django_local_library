<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

interface Author {
  id: number;
  first_name: string;
  last_name: string;
}


interface Book {
  id: number;
  title: string;
  summary: string;
  isbn: string;
  author: Author | null;
}


const route = useRoute();
const book = ref<Book | null>(null);
const loading = ref(true);

const fetchBookDetails = async () => {
  try {
    loading.value = true;
    const bookId = route.params.id;
    const response = await axios.get(`books/${bookId}`);
    book.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do livro:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBookDetails);
</script>

<template>
<SidebarComponent/>
<div class="page">
    <div class="page-wrapper">
        <div class="page-header d-print-none">
            <div class="container-xl">
                <div class="row g-2 align-items-center">
                    <div class="col">
                        <h1>Título: {{ book?.title }}</h1>
                        <h4 class="page-subtitle">Autor: {{ book?.author ? `${book.author.first_name} ${book.author.last_name}` : 'Desconhecido' }}</h4>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-body">
            <div class="container-xl">
                <div>
                    <h3>Sumário:</h3><p>{{ book?.summary }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped></style>