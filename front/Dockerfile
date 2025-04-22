# Imagem base com Node.js
FROM node:22-alpine AS build

# Diretório de trabalho
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copiar arquivos de configuração de dependências
COPY package.json ./
COPY pnpm-lock.yaml ./

# Instalar dependências
RUN pnpm install
# Copiar o código fonte
COPY . .

# Expor a porta padrão do servidor de desenvolvimento Vite (5173)
# Se estiver usando Vue CLI, a porta padrão seria 8080
EXPOSE 80

# Comando para iniciar o servidor de desenvolvimento com hot-reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]