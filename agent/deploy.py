import os
import re
import subprocess

def atualizar_arquivos_locais(ai_output):
    """Salva o código gerado nos arquivos do projeto Next.js."""
    print("   💾 Atualizando código fonte...")
    
    if not ai_output or 'app_config' not in ai_output:
        return False

    try:
        # Define caminho (funciona rodando da raiz ou da pasta agent)
        base_path = "." if os.path.exists("src") else ".."
        
        # 1. Salva AppConfig.ts
        # Limpa blocos de código markdown se houver
        clean_code = ai_output['app_config'].replace('```typescript', '').replace('```', '')
        
        config_path = f"{base_path}/src/utils/AppConfig.ts"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
            
        # 2. Atualiza Tailwind
        tw_path = f"{base_path}/tailwind.config.js"
        color = ai_output.get('primary_color', '#03A9F4')
        
        if os.path.exists(tw_path):
            with open(tw_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Substitui a cor 500 usando regex
            new_content = re.sub(r"500: '#.*?'", f"500: '{color}'", content)
            with open(tw_path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
        return True
    except Exception as e:
        print(f"   ❌ Erro ao salvar arquivos: {e}")
        return False

def deploy_vercel(cliente_nome):
    """Roda formatação e deploy na Vercel."""
    print("   🚀 Iniciando Deploy Vercel...")
    
    cwd = "." if os.path.exists("package.json") else ".."
    
    # 1. Formatar código (Prettier) - Essencial para não quebrar build
    subprocess.run("npm run format", shell=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Criar nome do projeto (slug limpo)
    slug = re.sub(r'[^a-z0-9-]', '', cliente_nome.lower().replace(' ', '-'))[:40]
    project_name = f"lp-{slug}"
    
    # 3. Deploy comando
    cmd = f"vercel --prod --yes --force --name {project_name}"
    
    try:
        # Timeout de 3 minutos
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=180)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            # Tenta encontrar URL limpa
            urls = re.findall(r'https://[^\s]+vercel.app', output)
            return urls[0] if urls else output
        else:
            return f"Erro Vercel: {result.stderr[:100]}..."
    except Exception as e:
        return f"Erro Script: {str(e)}"