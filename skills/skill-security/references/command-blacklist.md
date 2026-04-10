# Zararlı Komut Kara Listesi

## KESİN RED — Çalıştırma, Derhal Durdur

### Sistem Yıkımı
```bash
rm -rf /
rm -rf /*
rm -rf ~
dd if=/dev/zero of=/dev/sda
dd if=/dev/random of=/dev/sda
mkfs /dev/sda
mkfs.ext4 /dev/sda
> /dev/sda
shred /dev/sda
wipefs /dev/sda
```

### Fork Bomb / Kaynak Tükenmesi
```bash
:(){ :|:& };:
fork_bomb() { fork_bomb | fork_bomb & }
while true; do ./ & done
python3 -c "import os; [os.fork() for _ in iter(int,1)]"
```

### Uzak Kod Çalıştırma (RCE)
```bash
curl http://... | bash
curl http://... | sh
wget -O- http://... | bash
wget -O- http://... | sh
eval $(curl ...)
eval $(wget ...)
```

### Reverse Shell
```bash
nc -e /bin/sh
nc -e /bin/bash
ncat -e /bin/sh
bash -i >& /dev/tcp/
python3 -c "import socket..."  # reverse shell pattern
```

### Yetki Yükseltme
```bash
sudo su -
sudo bash
sudo -i
chmod 4755 /bin/bash  # SUID bash
chown root:root /tmp/x && chmod +s /tmp/x
```

### Toplu Veri Silme
```bash
find / -delete
find / -exec rm {} \;
find . -type f -delete
truncate -s 0 $(find / -type f)
```

---

## YÜKSEK RİSK — Onay Gerektirir

### Geniş Sistem Erişimi
```bash
find / -type f               # tüm dosya sistemi tarama
ls -laR /                    # recursive root listesi
cat /etc/shadow              # şifre hash'leri
cat /etc/passwd              # kullanıcı listesi
cat ~/.ssh/id_rsa            # özel SSH key
env                          # tüm environment (secret'lar olabilir)
printenv                     # tüm environment
set                          # tüm shell değişkenleri
```

### Process Yönetimi
```bash
kill -9 -1                   # tüm processleri öldür
killall -9                   # tüm processleri öldür
pkill -9 -u root             # root processlerini öldür
```

### Ağ Güvenliği
```bash
iptables -F                  # firewall kurallarını temizle
ufw disable                  # firewall kapat
nmap -sS                     # port tarama (stealth scan)
tcpdump                      # ağ trafiği dinleme
wireshark                    # ağ trafiği yakalama
```

### Kritik Sistem Dosyaları
```bash
cat /etc/sudoers
cat /etc/crontab
crontab -r                   # tüm cron işlerini sil
```

### Potansiyel Veri Kaybı
```bash
mv /* /dev/null
cp /dev/null important_file
truncate -s 0 *.db
```

---

## ORTA RİSK — İzleme Altında

### Dinamik Kod Çalıştırma (Input'a Bağlı)
```bash
eval "$user_input"
bash -c "$user_input"
sh -c "$user_input"
python3 -c "$user_code"
node -e "$user_script"
```

### Büyük Kaynak Kullanımı
```bash
yes > /dev/null              # CPU tükenmesi
cat /dev/urandom > file      # disk doldurma
stress --cpu 8               # CPU stresi
```

### Servis Yönetimi
```bash
systemctl stop              # servis durdurma
service stop                # servis durdurma
reboot                      # sistem yeniden başlatma
halt                        # sistem durdurma
shutdown                    # sistem kapatma
```

---

## GÜVENLİ — Onaysız Çalıştırılabilir

```bash
# Okuma
ls, cat, head, tail, grep, find (sınırlı dizin), wc
# Metin işleme
awk, sed, cut, tr, sort, uniq
# Bilgi toplama
pwd, whoami, date, uname (bilgi toplama için)
# Geliştirme
git status, git log, git diff (yazma değil)
# Dosya oluşturma (belirli dizinlerde)
mkdir, touch, cp (temp dizine)
```

---

## Dinamik Komut Tespiti

Aşağıdaki kalıplar varsa komut içeriğine bakılmaksızın onay gerektirir:

```python
# Python
os.system(variable)
subprocess.run(variable, shell=True)
exec(variable)
eval(variable)
__import__(variable)

# JavaScript/Node
eval(variable)
new Function(variable)
child_process.exec(variable)

# Shell
$()  # komut substitution + değişken
``   # backtick + değişken
```
