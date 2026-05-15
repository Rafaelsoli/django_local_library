<script setup lang="ts">
import SidebarComponent from '@/components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Alugados {
    id: number;
    due_back: string;
    status: string;
    imprint: string;
    titulo_livro: string;
}

const source = ref<Alugados[]>([]);
const loading = ref(true);

const fetchAlugados = async () => {
    try {
        loading.value = true;
        const response = await axios.get('/loans/mine');
        source.value = response.data;
    } catch (error) {
        console.error("Erro ao buscar livros alugados:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchAlugados);
</script>

<template>
<SidebarComponent/>
<div class="page">
    <div class="page-wrapper">
        <div class="page-header d-print-none">
            <div class="container-xl">
                <div class="row g-2 align-items-center">
                    <div class="col">
                        <h1>Cópias Alugadas</h1>
                        <h4 class="page-subtitle">Livros alugados por mim</h4>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-body">
            <div class="container-xl">
                <div v-for="alugados in source" :key="alugados.id">
                    <div class="card" style="max-width: 22rem; margin-top: 10px;">
                        <div class="card-body">
                            <h3 class="card-title mb-3">{{ alugados.titulo_livro }}</h3>
                            <div class="text-secondary mb-2">
                                Imprint: <span class="text-body font-weight-medium">{{ alugados.imprint }}</span>
                            </div>
                            <div>
                                <span class="text-secondary">Status:</span>
                                <span class="badge bg-blue-lt ms-1">{{ alugados.status }}</span>
                            </div>
                        </div>
                        <div class="card-footer text-secondary small bg-transparent border-top-0 pt-0">
                            Devolução: <span class="text-body fw-bold">{{ alugados.due_back }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>