<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// Função utilitária para pegar o CSRF token do Django
const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

interface Author {
  id: number;
  first_name: string;
  last_name: string;
}

interface BookInstance {
  id: string; // UUID vindo do Django
  imprint: string;
  status: string;
  due_back: string | null;
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
const instances = ref<BookInstance[]>([]); // Ref dedicada para armazenar as cópias isoladamente
const loading = ref(true);
const erroMensagem = ref<string | null>(null)
const acertoMensagem = ref<string | null>(null)

const fetchBookDetails = async () => {
  try {
    loading.value = true;
    const bookId = route.params.id;
    
    // Faz as duas requisições em paralelo para otimizar a performance
    const [bookResponse, instancesResponse] = await Promise.all([
      axios.get(`books/${bookId}`),
      axios.get(`books/${bookId}/instances`) // Nova rota focada do backend
    ]);

    book.value = bookResponse.data;
    instances.value = instancesResponse.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do livro e de suas cópias:", error);
  } finally {
    loading.value = false;
  }
};

const fazerEmprestimo = async (instanceId: string) => {
  try {
    const csrfToken = getCookie('csrftoken');
    
    await axios.post(`loans/${instanceId}/borrow`, {}, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    });
    acertoMensagem.value = "Emprestimo realizado com sucesso"
    
    await fetchBookDetails();
  } catch (error: any) {
    console.error("Erro ao pegar livro emprestado:", error);
    erroMensagem.value = "Erro ao fazer emprestimo" 
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
                        <div class="alert alert-danger alert-dismissible" role="alert" v-if="erroMensagem">
                          <div class="alert-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                              stroke-linecap="round" stroke-linejoin="round"
                              class="icon alert-icon icon-2">
                              <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />
                              <path d="M12 8v4" />
                              <path d="M12 16h.01" />
                            </svg>
                          </div>
                          {{erroMensagem}}
                          <a class="btn-close" data-bs-dismiss="alert" aria-label="close" @click="erroMensagem = ''"></a>
                        </div>
                        <div class="alert alert-success alert-dismissible" role="alert" v-if="acertoMensagem">
                        <div class="d-flex">
                          <div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon alert-icon" width="24"
                              height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                              fill="none" stroke-linecap="round" stroke-linejoin="round">
                              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                              <path d="M5 12l5 5l10 -10" />
                            </svg>
                          </div>
                          {{ acertoMensagem }}
                          <a class="btn-close" data-bs-dismiss="alert" aria-label="close" @click="acertoMensagem = ''"></a>
                        </div>
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
        <div class="page-body">
        <div class="container-xl">
          <h2 class="mb-3">Cópias</h2>
          <!-- <div class="card"> -->
            <!-- <div class="card-body"> -->
              <div v-if="instances && instances.length > 0">
                <div v-for="instance in instances" :key="instance.id" class="card mb-2">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div>
                            <h3 class="card-title mb-1">{{ instance.imprint }}</h3>
                            
                            <!-- Badges visuais baseados no status do Django -->
                            <span v-if="instance.status === 'a'" class="badge bg-success-lt">Disponível</span>
                            <span v-else-if="instance.status === 'o'" class="badge bg-warning-lt">Emprestado</span>
                            <span v-else-if="instance.status === 'm'" class="badge bg-danger-lt">Manutenção</span>
                            <span v-else class="badge bg-secondary-lt">Reservado</span>

                            <p v-if="instance.due_back" class="text-muted small mt-2 mb-0">
                              Data de Devolução: {{ instance.due_back }}
                            </p>
                        </div>
                        <div>
                          <button 
                            v-if="instance.status === 'a'" 
                            @click="fazerEmprestimo(instance.id)" 
                            class="btn btn-primary btn-sm"
                          >
                            Pegar Emprestado
                          </button>
                        </div>
                    </div>
                </div>
              </div>
              
              <div v-else class="text-muted">
               Este livro não possui cópias na biblioteca.
              </div>
            <!-- </div> -->
          <!-- </div> -->
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped></style>