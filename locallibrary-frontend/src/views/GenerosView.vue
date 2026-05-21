<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};


interface Genre {
  name: string;
}

const route = useRoute();
const genres = ref<Genre[]>([]);
const loading = ref(true);

const fetchGenres = async () => {
  try {
    loading.value = true;
    const response = await axios.get('genres');
    genres.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar gêneros:", error);
  } finally {
    loading.value = false;
  }
};

const addGenre = async () => {
  const genreName = prompt("Digite o nome do novo gênero:");
  if (!genreName) return;
  const csrfToken = getCookie('csrftoken');
  try {
    await axios.post('genres', { name: genreName }, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    });
    alert("Gênero adicionado com sucesso!");
    await fetchGenres();
  } catch (error) {
    console.error("Erro ao adicionar gênero:", error);
    alert("Ocorreu um erro ao adicionar o gênero. Verifique o console para mais detalhes.");
  }
};

onMounted(fetchGenres);
</script>

<template>
    <SidebarComponent/>
    <div class="page" v-if="!loading">
        <div class="page-wrapper">
            <div class="page-header d-print-none">
                <div class="container-xl">
                    <div class="row g-2 align-items-center">
                        <div class="col">
                            <h1 class="page-title">Gêneros Literários</h1>
                        </div>
                        <div class="col-auto ms-auto d-print-none">
                            <button class="btn btn-primary" @click="addGenre">Adicionar Gênero</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="page-body">     
                <div class="container-xl">
                    <div v-if="genres.length > 0" class="list-group">
                        <div v-for="genre in genres" :key="genre.name" class="list-group-item">
                            {{ genre.name }}
                        </div>
                    </div>
                    <div v-else class="text-muted">
                        Nenhum gênero encontrado na biblioteca.
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>