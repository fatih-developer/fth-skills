# Güvenilir API ve Domain Beyaz Listesi (Whitelist)

Aşağıdaki liste, skill'lerin (`skill-security` denetiminde) herhangi bir checkpoint (kullanıcı onayı) olmadan `HTTPS POST/GET` istekleri atabileceği varsayılan servisleri tanımlar.
Bu listede olmayan adreslere yapılan trafik, Trust skoruna bağlı olarak engellenir veya özel kullanıcı onayı ister.

## Güvenilir Genel Sağlayıcılar

### Bulut ve Altyapı
- `*.amazonaws.com` (AWS API'leri)
- `*.googleapis.com` (Google Cloud & Workspace API)
- `*.azure.com` (Azure Hizmetleri)
- `*.cloudflare.com` (Cloudflare API)

### AI ve Dil Modelleri
- `api.anthropic.com` (Claude API)
- `api.openai.com` (OpenAI API)
- `api.gemini.google.com` (Google Gemini)
- `*.minimax.chat` (Minimax Açık Kaynak / Modelleri)

### VCS ve Geliştirme Araçları
- `api.github.com` (GitHub API)
- `gitlab.com/api/*` (GitLab API)
- `bitbucket.org/api/*` (Bitbucket)

### Veritabanı ve Auth (BaaS)
- `*.supabase.co` (Supabase API)
- `*.firebaseio.com` (Firebase API)
- `*.auth0.com` (Auth0 Token Endpointler)

## Kural Seti:
1. Sadece **HTTPS** veya **WSS** güvenliğine sahip bağlantılar white-list'te kabul edilebilir.
2. HTTP (şifresiz) hiçbir zaman otomatik güvenilir kabul edilmez.
3. Bu public adresler dışında projeye (örneğin sizin kendi şirket ağınızdaki serverlara) özel sunucularınız varsa bu listeye kolaylıkla ekleyebilirsiniz.
