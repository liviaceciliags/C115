# Trabalho Mininet — Topologia Linear com 6 Switches

## Descrição
Criar uma **topologia linear com 6 switches** utilizando o **Mininet**, com endereços MAC padronizados, largura de banda de 25 Mbps e controlador padrão.  

---

## Passos

### 1. Criar a topologia
```bash
sudo mn --topo=linear,6 --mac --link tc,bw=25
```

### 2. Verificar informações dos nós
Dentro do terminal do Mininet (`mininet>`):
```bash
nodes
net
dump
h1 ifconfig -a
s1 ifconfig -a
sh ovs-ofctl show s1
```

### 3. Testar conectividade
```bash
pingall
h1 ping -c 5 h2
```

### 4. Teste de desempenho (iperf)
Host 1 será o **servidor TCP** e Host 2 o **cliente**.
```bash
h1 iperf -s -p 5555 -i 1 &
h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```
- `-s`: servidor  
- `-c`: cliente  
- `-p`: porta 5555  
- `-i 1`: relatório a cada segundo  
- `-t 15`: duração de 15 segundos  

### 5. Finalizar
```bash
exit
sudo mn -c
```

---

