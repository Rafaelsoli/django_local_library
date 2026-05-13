<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import SidebarComponent from '@/components/SidebarComponent.vue';

const router = useRouter();
const loading = ref(false);
const erro = ref('');

// 1. Dados do formulário
const form = reactive({
    username: '', // Django usa username por padrão
    password: ''
});

// 2. Função de Login
const handleLogin = async () => {
    loading.value = true;
    erro.value = '';
    
    try {
        // Envia para o seu @api.post("/login")
        const response = await axios.post('login', {
            username: form.username,
            password: form.password
        });

        if (response.data.success) {
            // Login ok! Redireciona para a home
            router.push('/');
        }
    } catch (e: any) {
        console.error(e);
        if (e.response?.status === 401) {
            erro.value = 'Usuário ou senha incorretos.';
        } else {
            erro.value = 'Erro ao conectar com o servidor.';
        }
    } finally {
        loading.value = false;
    }
};
</script>

<template>
<SidebarComponent></SidebarComponent>
<div class="page">
    <div class="page-wrapper">
        <div class="container-fluid d-flex align-items-center justify-content-center" style="min-height: 100vh;">
            <div class="card card-md" style="width: 28rem;">
                <div class="card-body">
                    <h1 class="card-title text-center mb-4">Login</h1>
                    <p class="card-subtitle text-center mb-4">Faça login para acessar sua conta.</p>
                    
                    <!-- Alerta de Erro -->
                    <div v-if="erro" class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>

                    <form @submit.prevent="handleLogin">
                        <div class="mb-3">
                            <label class="form-label">Usuário</label>
                            <input 
                                v-model="form.username" 
                                type="text" 
                                class="form-control" 
                                placeholder="Digite seu usuário"
                                required
                            >
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Senha</label>
                            <input 
                                v-model="form.password" 
                                type="password" 
                                class="form-control" 
                                placeholder="Digite sua senha"
                                required
                            >
                        </div>
                        <div class="form-footer">
                            <button 
                                type="submit" 
                                class="btn btn-primary w-100"
                                :disabled="loading"
                            >
                                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                Entrar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
/* Removemos o SidebarComponent da tela de login para ficar mais limpo */
.page {
    background-color: #f4f6fa;
}
</style>